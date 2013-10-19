#!/bin/bash

# a simple script to remove temp files and restart the server

python serve.py
sleep 2s
/bin/bash runserver.sh "$@"
