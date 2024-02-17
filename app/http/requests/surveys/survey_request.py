from marshmallow import Schema, fields, validate ,ValidationError, validates_schema
from app.rules.validate import validate_discussion, validate_message


class CreateSurveySchema(Schema):
    
    discussion_id = fields.String(required=True, validate=[validate_discussion])
    options = fields.List(fields.String(required=True))
    question = fields.String(required=True)

class UpdateSurveySchema(Schema):
    
    action = fields.String(required=True, validate=validate.OneOf(['ASK_SURVEY']))
    option_id = fields.String(required=True)
    is_selected = fields.Boolean(required=True)


    