from asyncio import sleep, EventLoop
from sqlite3 import IntegrityError
from datetime import UTC, datetime

from data import create_user, redis_client, stream, user_exists

duration = 30

async def main():
    while True:
        stream_data = redis_client.xread(streams={stream: '10'}, block=2000)
        for _, requests in stream_data:
            for key, payload in requests:
                email = payload.get(b'email')
                if user_exists(email):
                    print(f"Request {key} is a duplicate. Dropping. [ {email} ]")
                    delete_item(stream, key, True)
                    continue
                try:
                    create_user(payload)
                except IntegrityError:
                    print(f"{email} is a duplicate and has not been caught somehow! Deleting.")
                    delete_item(stream, key)
        print(f"[{datetime.now(UTC)}] - Sleeping for {duration}s.")
        await sleep(duration)


def delete_item(stream: str, _id: str, post_insert=False) -> None:
    if post_insert:
        print(f"Consumed {_id} for user creation. Deleting from stream")
    else:
        print(f"Deleting {_id} from stream")
    redis_client.xdel(stream, _id)


if __name__ == "__main__":
    loop = EventLoop()
    loop.run_until_complete(main())
