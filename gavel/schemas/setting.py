from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from gavel.models import Setting, db


class SettingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Setting
        sqla_session = db.session
        load_instance = True