from marshmallow import Schema, fields, validate ,ValidationError, validates_schema
from app.rules.validate import validate_discussion

class MemberSchema(Schema):
    userId = fields.String(required=True,validate=[validate_discussion])
    isAdmin = fields.Boolean(required = True)
    
class CreateDiscussionSchema(Schema):
    
    name = fields.String(required=False)
    description = fields.String(required=False)
    tag = fields.String(required=True, validate=validate.OneOf(['GROUP','PRIVATE']))
    members  = fields.List(fields.Nested(MemberSchema))