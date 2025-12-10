from datetime import datetime
from json import dumps, loads
from flask import Flask, request

from data import redis_client, stream
from utils import logger

app = Flask(__name__)

def main():
    app.run()
    
@app.post('/')
def register():
    data = loads(request.data)
    if not data.get("email"):
        return dumps({
            "message": "Missing email"
        }), 400
    if not data.get("password"):
        return dumps({
            "message": "Missing password"
        }), 400
    created_at = datetime.utcnow().timestamp() * 1000
    data.update({"created_at": created_at})
    stream_key = redis_client.xadd(stream, data)
    app.logger.info(f"Pushed to stream. Key - {stream_key}")
    return dumps(data)


if __name__ == "__main__":
    main()
