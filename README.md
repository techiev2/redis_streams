# Redis streams with Python

This repository is an implementation of Redis streams usage in Python. The idea is to have a simple boilerplat to get started with Redis streams.

## Environment
The repo is built with Python 3.14 and dependencies managed via uv. If you don't use uv, you can use the requirements.txt enclosed.

## Functionality

1. A flask API exposes a register end point at "/" over HTTP POST.
2. If email and password are provided, the API adds the payload to a stream `user:signedup`
3. A consumer wakes up every `2 seconds`(configured via a variable in consumer) to pull the last entries from the stream.
4. For each entry, consumer checks if the email exists in the DB via a lean query.
5. a. If the email doesn't exist, consumer calls a helper to insert the user into the users table and deletes the key from the table.
5. b. If the email exists, then consumer proceeds with deleting the key from the stream.

Deleting the key from the stream goes against an append-only log nature but is a design choice I made for a particular workflow I am testing. It is not the usual and can be dropped in your case.