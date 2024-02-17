from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class CreateUserSchema(Schema):
    
    firstname = fields.String(required=True,validate=validate.Length(min=1,max=255))
    lastname = fields.String(required=False,validate=validate.Length(max=255))
    email = fields.Email(required=True)
    password = fields.String(required=True,validate=validate.Length(min=8,max=255))
    
    
class SearchUserInputSchema(Schema):
    
    search = fields.String(
        required = False, 
        allow_none=True, 
        validate=[
            # validate.Length(min=1,max=255),
            validate.Regexp(regex="^[a-zA-Z0-9_.-]*$")
        ]
    )
    page = fields.Integer(required=False)
    

class EditUserSchema(Schema):
    
    firstname = fields.String(required=False,validate=validate.Length(min=1,max=255))
    lastname = fields.String(required=False,validate=validate.Length(max=255))
    email = fields.Email(required=False)
    status = fields.String(required=False, allow_none=True)
    photo = fields.String(required=False, allow_none=True)
    action = fields.String(required=True, validate=validate.OneOf(['UPDATE_INFOS','CHANGE_PASSWORD']))

    current_password = fields.String(required=False, allow_none=True)
    new_password = fields.String(required=False, allow_none=True)