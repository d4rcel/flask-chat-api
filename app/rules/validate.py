from urllib.parse import urlparse
from config import Config
from marshmallow import ValidationError
from datetime import datetime, date

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