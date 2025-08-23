from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from gavel.models import Annotator, db

class AnnotatorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Annotator
        sqla_session = db.session
        load_instance = True