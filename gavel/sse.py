import queue
import threading
import json
from flask import Response, stream_with_context

_subscribers = []
_subscribers_lock = threading.Lock()


def subscribe():
    q = queue.Queue(maxsize=256)
    with _subscribers_lock:
        _subscribers.append(q)
    return q


def unsubscribe(q):
    with _subscribers_lock:
        try:
            _subscribers.remove(q)
        except ValueError:
            pass


def publish(event_type, data):
    message = _format_sse(event_type, data)
    with _subscribers_lock:
        dead = []
        for q in _subscribers:
            try:
                q.put_nowait(message)
            except queue.Full:
                dead.append(q)
        for q in dead:
            _subscribers.remove(q)


def _format_sse(event_type, data):
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


def create_sse_response(auth_check):
    def generate():
        q = subscribe()
        try:
            yield _format_sse("connected", {"status": "ok"})
            while True:
                try:
                    message = q.get(timeout=30)
                    yield message
                except queue.Empty:
                    yield ": keepalive\n\n"
        finally:
            unsubscribe(q)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
        }
    )
