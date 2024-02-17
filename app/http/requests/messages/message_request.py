from marshmallow import Schema, fields, validate ,ValidationError, validates_schema
from app.rules.validate import validate_discussion, validate_message


class SendMessageSchema(Schema):
    
    text = fields.String(required=False)
    discussion_id = fields.String(required=True, validate=[validate_discussion])
    response_to_msg_id = fields.String(required=False, validate=[validate_message])
    survey_id = fields.String(required=False)

class ReactionToMessageSchema(Schema):
    
    emoji = fields.String(required=True)
    action = fields.String(required=True,validate=validate.OneOf(['EMOJI_REACTION']))

class MessageSchema(Schema):
    
    discussion_id = fields.String(required=True, validate=[validate_discussion])
    