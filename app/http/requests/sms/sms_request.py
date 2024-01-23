from marshmallow import Schema, fields, validate


class SmsSchema(Schema):
 
    # phone_number = fields.Email(required=True,validate=validate.Regexp())
    phone_number = fields.Integer(required=True)
    user_id = fields.Integer(required=False)