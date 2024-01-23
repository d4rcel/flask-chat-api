from flask import render_template
from celery_holder import celery
from config import EmailConfig, Config
import requests
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from mail import api_instance

@celery.task(name='send_reset_password_code_job') 
def send_reset_password_code_job(kwargs): 
    
    if kwargs.get("email"):
        
        data = {
            'email': kwargs.get("email"),
            'username': kwargs.get('username'),
            'code': kwargs.get('code'),
        }
        
        # requests.post('https://mailapi.scoopchat.app/api/send/reset/password/mail', )
        
        
        subject = "Reset Password"
        sender = {
            "name": EmailConfig.EMAIL_SENDER_NAME,
            "email": EmailConfig.EMAIL_SENDER
        }
        
        replyTo = {
            "name": EmailConfig.EMAIL_SENDER_NAME,
            "email": EmailConfig.EMAIL_SENDER
        }
        
        html_content = render_template(
            'reset_password_mail.html',
            username=kwargs.get('username'),
            code=kwargs.get('code')
        )
        to = [{
            "email":kwargs.get("email"),
            "name":kwargs.get('username')
        }]
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            reply_to=replyTo,
            # headers=headers,
            html_content=html_content,
            sender=sender,
            subject=subject
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            # print(api_response)
        except ApiException as e:
            pass
    elif kwargs.get('phone_number'):
        
        payload = {
            'text': f"Bonjour chers utilisateur, Voici votre code de confirmation WeScoop : {kwargs.get('code')} À bientôt. Team WeScoop.",
            'to': kwargs.get('phone_number').replace('+', '').replace(" ",''),
            'sender': 'Wescoop',
            'token': Config.SMS_API_KEY
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        requests.get('https://api.smsfactor.com/send', params=payload, headers=headers)
        
@celery.task(name="send_verify_email_code_job")
def send_verify_email_code_job(kwargs):
    
    data = {
        'email': kwargs.get("email"),
        'username': kwargs.get('username'),
        'code': kwargs.get('code'),
    }
        
    # requests.post('https://mailapi.scoopchat.app/api/send/verify/email/mail', data=payload)
    
    subject = "Vérification de l'adresse email"
    sender = {
        "name": EmailConfig.EMAIL_SENDER_NAME,
        "email": EmailConfig.EMAIL_SENDER
    }
    
    replyTo = {
        "name": EmailConfig.EMAIL_SENDER_NAME,
        "email": EmailConfig.EMAIL_SENDER
    }
        
    html_content = render_template(
        'verify_email_mail.html',
        username=kwargs.get('username'),
        code=kwargs.get('code')
    )
    to = [{
        "email":kwargs.get("email"),
        "name":kwargs.get('username')
    }]
        
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        reply_to=replyTo,
        # headers=headers,
        html_content=html_content,
        sender=sender,
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        # print(api_response)
    except ApiException as e:
        pass
        # print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
