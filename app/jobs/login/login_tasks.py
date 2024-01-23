from app.models.users.user_model import  UserHasDevice, Device
from db import db_session_master
from celery_holder import celery

@celery.task(name='login_job') 
def login_job(kwargs): 

    if kwargs.get('device_id') is not None:
        try:
            db_session_master.query(UserHasDevice).filter(UserHasDevice.device_id==kwargs.get('device_id')).delete()
            user_has_device = UserHasDevice(kwargs.get('user_id'), kwargs.get('device_id'))
            db_session_master.add(user_has_device)
            db_session_master.commit()
        except:
            db_session_master.rollback()
            
    if kwargs.get('hardware_device_id') is not None:
        try:
            db_session_master.query(Device)\
                .filter(
                    Device.device_id==kwargs.get('hardware_device_id')
                ).delete()
            device = Device(user_id=kwargs.get('user_id'),device_id=kwargs.get('hardware_device_id'))
            db_session_master.add(device)
            db_session_master.commit()
        except:
            db_session_master.rollback()
        
@celery.task(name='logout_job') 
def logout_job(kwargs): 

    if kwargs.get('device_id') is not None:
        try:
            db_session_master.query(UserHasDevice).filter(UserHasDevice.device_id==kwargs.get('device_id')).delete()
            db_session_master.commit()
        except:
            db_session_master.rollback()
        
    if kwargs.get('hardware_device_id') is not None:
        try:
            db_session_master.query(Device)\
                .filter(
                    Device.device_id==kwargs.get('hardware_device_id')
            ).delete()
            db_session_master.commit()
        except:
            db_session_master.rollback()
       