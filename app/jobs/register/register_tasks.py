from redis_client import username_redis_client, user_redis_client, mail_redis_client
from app.models.users.user_model import UserHasSetting, UserHasMessageSetting, UserHasCoin, UserHasDevice, Device, User
from db import db_session_master
from celery_holder import celery
# from sqs import sqs
from elastic_search import es 
from config import Config

@celery.task(name='register_job') 
def register_job(kwargs): 
    
    if kwargs.get('user').get('id') != None:
        user_redis_client.set('prod_api_database_user_id_'+str(kwargs.get('user').get('id')),kwargs.get('user').get('id'))
    
    if kwargs.get('user').get('username') != None:
        username_redis_client.set('prod_api_database_username_'+str(kwargs.get('user').get('username')),kwargs.get('user').get('username'))
        
    if kwargs.get('user').get('email') != None:
        mail_redis_client.set('prod_api_database_email_'+str(kwargs.get('user').get('email')),kwargs.get('user').get('email'))
        
    user_has_setting = UserHasSetting(kwargs.get('user').get('id'))
    user_has_message_setting = UserHasMessageSetting(kwargs.get('user').get('id'))
    user_has_coin = UserHasCoin(kwargs.get('user').get('id'))
    
    # print(kwargs.get('user'))
    add_user_in_elasticsearch_job.delay(kwargs.get('user').get('id'))

    db_session_master.add(user_has_setting)
    db_session_master.add(user_has_message_setting)
    db_session_master.add(user_has_coin)
    db_session_master.commit()

@celery.task(name='add_user_in_elasticsearch_job') 
def add_user_in_elasticsearch_job(user_id): 

    # print(user_id)
    user  = db_session_master.query(User).filter(User.id==user_id).first()
    
    es.index(
        index=Config.ELASTICSEARCH_INDEX,
        id=user_id,
        document=user.to_json(),
    )
    
    db_session_master.commit()