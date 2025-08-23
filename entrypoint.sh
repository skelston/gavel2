#!/bin/sh
python initialize.py && exec gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:$PORT gavel:app