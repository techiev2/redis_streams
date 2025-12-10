__all__ = ("redis_client", "cursor", "connection", "create_user", "user_exists")

import sqlite3

from redis.client import Redis

redis_client = Redis()
connection = sqlite3.connect("signups.db")
stream = "user:signedup"

cursor = connection.cursor()
cursor.execute("""create table if not exists users(
    id int PRIMARY KEY,
    email text not null unique,
    password text not null,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp
)""")
cursor.execute("""
    create index if not exists user_email on users(email)
""")



def user_exists(email: str) -> bool:
    [count] = cursor.execute('select count(1) as count from users where email = ?', (email,)).fetchone()
    return count > 0


def create_user(data):
    email = data.get(b"email")
    password = data.get(b"password")
    cursor.execute ("insert into users(email, password) values(?, ?)", (email, password))
    connection.commit()
    print(f"Created user for {email}")
