from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from gavel.models import Flag, db

class FlagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Flag
        sqla_session = db.session
        load_instance = True