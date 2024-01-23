from app.models.users.user_model import User
from db import db
from celery_holder import celery
from config import Config
import requests

@celery.task(name='send_sms_job') 
def send_sms_job(kwargs): 
    payload = {
        'text': f"Votre code de validation WeScoop est: {kwargs.get('code')}",
        'to': kwargs.get('phone_number'),
        'sender': 'Wescoop',
        'token': Config.SMS_API_KEY
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    r = requests.get('https://api.smsfactor.com/send', params=payload, headers=headers)
        
    