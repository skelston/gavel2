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


@app.context_processor
def inject_context():
    return dict(
      virtual=settings.VIRTUAL_EVENT,
      finished_button_text=str("Finish Review" if settings.VIRTUAL_EVENT else "Done With Visit"),
      debug_state=settings.DEBUG,
    )


from gavel.models import db, ma

from gavel.models import *
from gavel.schemas import *

db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)

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