# Redis streams with Python

This repository is an implementation of Redis streams usage in Python. The idea is to have a simple boilerplat to get started with Redis streams.

## Environment
The repo is built with Python 3.14 and dependencies managed via uv. If you don't use uv, you can use the requirements.txt enclosed.

## Functionality

1. A flask API exposes a register end point at "/" over HTTP POST.
2. If email and password are provided, the API adds the payload to a stream `user:signedup`
