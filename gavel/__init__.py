# Copyright (c) 2015-2018 Anish Athalye (me@anishathalye.com)
#
# This software is released under AGPLv3. See the included LICENSE.txt for
# details.

import gevent.monkey
gevent.monkey.patch_all()

import os

from flask import Flask
from flask_compress import Compress
from flask_minify import minify
from flask_socketio import SocketIO
from flask_json import FlaskJSON


BASE_DIR = os.path.dirname(__file__)

COMPRESS_MIMETYPES = [
  'text/html',
  'text/css',
  'text/xml',
  'application/json',
  'application/javascript'
]
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500

compress = Compress()

JSON = FlaskJSON()


def start_app():
  gavel = Flask(__name__)
  
  JSON.init_app(gavel)

  compress.init_app(gavel)

  minify(app=gavel)

  gavel.url_map.strict_slashes = False

  return gavel


app = start_app()

app.config['DEBUG'] = os.environ.get('DEBUG', False)

import gavel.settings as settings

app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = settings.SECRET_KEY

from flask_assets import Environment, Bundle

assets = Environment(app)
assets.url = app.static_url_path

# CSS bundle for Tailwind-generated CSS
css_bundle = Bundle(
    'generated.css',           # Your Tailwind output file
    depends='**/*.css',        # Rebuild if any CSS changes
    output='all.css'           # This will be generated in /static
)
admin_js_bundle = Bundle(
    'js/admin/admin_live.js',
    'js/admin/admin_service.js',
    depends='**/*.js',
    filters='rjsmin',
    output='admin_all.js'
)

# Register bundles
assets.register('all', css_bundle)
assets.register('admin_js', admin_js_bundle)

# Build automatically in debug mode
if app.debug:
    css_bundle.build(force=True)
    admin_js_bundle.build(force=True)

@app.context_processor
def inject_context():
    return dict(
      virtual=settings.VIRTUAL_EVENT,
      finished_button_text=str("Finish Review" if settings.VIRTUAL_EVENT else "Done With Visit"),
      debug_state=settings.DEBUG,
    )

from celery import Celery

app.config['CELERY_BROKER_URL'] = settings.BROKER_URI
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from gavel.models import db, ma

from gavel.models import *
from gavel.schemas import *

db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)

SOCKETIO_REDIS_URL = settings.BROKER_URI
async_mode="gevent"

socketio = SocketIO(app, async_mode=async_mode, message_queue=SOCKETIO_REDIS_URL, async_handlers=True)

import gavel.template_filters  # registers template filters

import gavel.controllers  # registers controllers

# send usage stats
import gavel.utils

gavel.utils.send_telemetry('gavel-boot', {
  'base-url': settings.BASE_URL or '',
  'min-views': settings.MIN_VIEWS,
  'timeout': settings.TIMEOUT,
  'disable-email': settings.DISABLE_EMAIL
})