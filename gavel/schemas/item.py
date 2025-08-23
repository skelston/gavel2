from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from gavel.models import Item, db

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        sqla_session = db.session
        load_instance = True