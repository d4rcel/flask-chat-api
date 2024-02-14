from urllib.parse import urlparse
from config import Config
from marshmallow import ValidationError
from datetime import datetime, date
from bson.objectid import ObjectId
from app.models.contacts.contact_model import Contact
from app.models.discussions.discussion_model import Discussion

def validate_link(n):
    if urlparse(n).netloc in  Config.BLOCKED_LINKS:
        raise ValidationError("This link is blocked in our app.")
    
def validate_birthday(birthdate):
    
    today = date.today()
    age = today.year - birthdate.year
    # print(age <= 17 and ((today.month, today.day) >= (birthdate.month, (birthdate.day+1))))
    # print(age)
    
    if age <= 17 and ((today.month, today.day) >= (birthdate.month, (birthdate.day+1))):
        raise ValidationError("Sorry, you must be at least 17 years old to register.") 
    
def validate_contact(contact_id):
    try:
        id = ObjectId(contact_id) 
        contact =  Contact.objects(_id=contact_id).first()
        if contact is None:
            raise ValidationError('Contact doesn\'t not exist in our system')
    except :
        raise ValidationError('Contact doesn\'t not exist in our system')

def validate_discussion(discussion_id):
    try:
        id = ObjectId(discussion_id) 
        discussion =  Discussion.objects(_id=discussion_id).first()
        if discussion is None:
            raise ValidationError('Discussion doesn\'t not exist in our system')
    except :
        raise ValidationError('Discussion doesn\'t not exist in our system')
