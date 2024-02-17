from marshmallow import Schema, fields, validate
from app.rules.validate import validate_contact,validate_user

class CreateContactSchema(Schema):
    
    user2Id  = fields.String(required = True, validate=[validate_user])

class UpdateContactSchema(Schema):

    action = fields.String(required=True, validate=validate.OneOf(['BLOCKED_CONTACT','ANSWER_TO_REQUEST']))
    status = fields.String(required=True, validate=validate.OneOf(['PENDING','VALIDATED']))
    

class ContactSchema(Schema):

    status = fields.String(required=True, validate=validate.OneOf(['PENDING','VALIDATED']))
    user1Id  = fields.String(required = True, validate=[validate_user])
    user2Id  = fields.String(required = True, validate=[validate_user])

