from marshmallow import Schema, fields, validate ,ValidationError, validates_schema
from app.rules.validate import validate_discussion, validate_user

class MemberSchema(Schema):
    userId = fields.String(required=True,validate=[validate_user])
    isAdmin = fields.Boolean(required = True)
    
class CreateGroupDiscussionSchema(Schema):
    
    name = fields.String(required=False)
    description = fields.String(required=False)
    tag = fields.String(required=True, validate=validate.OneOf(['GROUP','PRIVATE']))
    members  = fields.List(fields.Nested(MemberSchema))
    
class DiscussionSchema(Schema):
    
    is_pined = fields.Boolean(required=False)
    is_archived = fields.Boolean(required=False)
    
class UpdateDiscussionSchema(Schema):
    
    action = fields.String(required=True, validate=validate.OneOf(['ADD_USERS_GROUP','UPDATE_GROUP_INFO','ARCHIVED','PINED','MUTED','REMOVE_USERS_GROUP','LEAVE_GROUP']))
    add_users = fields.List(fields.String(required=True, validate=[validate_user]))
    name = fields.String(required=False)
    description = fields.String(required=False)
    is_pined = fields.Boolean(required=False)
    is_archived = fields.Boolean(required=False)
    is_muted = fields.Boolean(required=False)
    remove_users = fields.List(fields.String(required=True, validate=[validate_user]))