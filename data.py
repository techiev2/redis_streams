__all__ = ("redis_client", "cursor", "connection")

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