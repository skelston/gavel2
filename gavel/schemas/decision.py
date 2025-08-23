from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from gavel.models import Decision, db

class DecisionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Decision
        sqla_session = db.session
        load_instance = True