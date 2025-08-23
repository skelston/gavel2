#!/bin/sh
python initialize.py && exec gunicorn -b 0.0.0.0:$PORT gavel:app -w 3