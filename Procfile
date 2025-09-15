worker: PYTHONUNBUFFERED=true celery -A gavel:celery worker -E -P gevent --loglevel=info
web: python initialize.py && gunicorn -k gevent gavel:app --workers=3 --bind 0.0.0.0:$PORT