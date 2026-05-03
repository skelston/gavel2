from gavel import app
from gavel.constants import *
from gavel.models import *
from gavel.schemas import ItemSchema, AnnotatorSchema, FlagSchema, SettingSchema
import gavel.utils as utils
import gavel.sse as sse
from sqlalchemy import event
from sqlalchemy import (or_, not_)
from flask import json, request, jsonify

item_schema = ItemSchema()
annotator_schema = AnnotatorSchema()
flag_schema = FlagSchema()
setting_schema = SettingSchema()


def standardize(target):
  try:
    name = target.__tablename__
    if str(name) == 'annotator':
      return {
        'type': name,
        'target': json.dumps(injectAnnotator(target, annotator_schema.dump(target)))
      }
    elif str(name) == 'flag':
      return {
        'type': name,
        'target': json.dumps(injectFlag(target, flag_schema.dump(target)))
      }
    elif str(name) == 'item':
      return {
        'type': name,
        'target': json.dumps(injectItem(target, item_schema.dump(target)))
      }
    elif str(name) == 'setting':
      settings = Setting.query.all()
      return {
        'type': name,
        'target': json.dumps([setting_schema.dump(it) for it in settings])
      }
    else:
      return {
        'type': name,
        'target': json.dumps(target.to_dict())
      }
  except Exception as e:
    print(str(e))
    return {
      'type': "ERROR",
      'target': json.dumps({'error': 'true'})
    }


def injectAnnotator(target, target_dumped):
  count = Decision.query.filter(Decision.annotator_id == target.id).count()
  target_dumped.update({
    'votes': count
  })
  return target_dumped


def injectFlag(target, target_dumped):
  target_dumped.update({
    'item_name': target.item.name,
    'item_location': target.item.location,
    'annotator_name': target.annotator.name
  })
  return target_dumped


def injectItem(target, target_dumped):
  assigned = Annotator.query.filter(Annotator.next == target).all()
  viewed_ids = {i.id for i in target.viewed}
  if viewed_ids:
    skipped = Annotator.query.filter(
      Annotator.ignore.contains(target) & ~Annotator.id.in_(viewed_ids)
    ).count()
  else:
    skipped = Annotator.query.filter(Annotator.ignore.contains(target)).count()

  viewed = len(target.viewed)

  target_dumped.update({
    'viewed': viewed,
    'votes': Decision.query.filter(or_(Decision.winner_id == target.id, Decision.loser_id == target.id)).distinct(Decision.id).count(),
    'skipped': skipped
  })
  return target_dumped


@app.route('/admin/events')
@utils.requires_auth
def sse_stream():
  return sse.create_sse_response(None)


@app.route('/admin/api/annotator-updated', methods=['POST'])
@utils.requires_auth
def annotator_updated_confirmed():
  data = request.get_json()
  try:
    ignore_ids = {i['id'] for i in data['ignore']}
    items = Item.query.filter(Item.id.in_(ignore_ids))
    for i in items:
      sse.publish(ITEM_UPDATED, {'type': "item", 'target': json.dumps(injectItem(i, item_schema.dump(i)))})
  except Exception:
    pass
  return jsonify({"status": "ok"})


@event.listens_for(Annotator, 'after_insert')
def annotator_listen_insert(mapper, connection, target):
  sse.publish(ANNOTATOR_INSERTED, standardize(target))

@event.listens_for(Annotator, 'after_update')
def annotator_listen_modify(mapper, connection, target):
  sse.publish(ANNOTATOR_UPDATED, standardize(target))

@event.listens_for(Annotator, 'after_delete')
def annotator_listen_delete(mapper, connection, target):
  sse.publish(ANNOTATOR_DELETED, {"target": json.dumps(annotator_schema.dump(target))})

@event.listens_for(Item, 'after_insert')
def item_listen_insert(mapper, connection, target):
  sse.publish(ITEM_INSERTED, standardize(target))

@event.listens_for(Item, 'after_update')
def item_listen_modify(mapper, connection, target):
  sse.publish(ITEM_UPDATED, standardize(target))

@event.listens_for(Item, 'after_delete')
def item_listen_delete(mapper, connection, target):
  sse.publish(ITEM_DELETED, {"target": item_schema.dump(target)})

@event.listens_for(Flag, 'after_insert')
def flag_listen_insert(mapper, connection, target):
  sse.publish(FLAG_INSERTED, standardize(target))

@event.listens_for(Flag, 'after_update')
def flag_listen_update(mapper, connection, target):
  sse.publish(FLAG_UPDATED, standardize(target))

@event.listens_for(Flag, 'after_delete')
def flag_listen_delete(mapper, connection, target):
  sse.publish(FLAG_DELETED, {"target": json.dumps(flag_schema.dump(target))})

@event.listens_for(Setting, 'after_insert')
def setting_listen_insert(mapper, connection, target):
  sse.publish(SETTING_INSERTED, standardize(target))

@event.listens_for(Setting, 'after_update')
def setting_listen_update(mapper, connection, target):
  sse.publish(SETTING_UPDATED, standardize(target))
