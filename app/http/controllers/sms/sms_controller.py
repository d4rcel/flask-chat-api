from app.http.requests.sms.sms_request import SmsSchema
from app.utils.common import generate_response, request_to_json
from app.models.users.user_model import UserHasSetting
from db import db_session_master, db_session_slave
from app.utils.http_code import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST
import random
from app.jobs.sms.sms_tasks import send_sms_job
from app.jobs.graylog.graylog_tasks import send_message_to_sqs_job

def send_sms(request,input_data):
    
    try:
        validator = SmsSchema()
        errors = validator.validate(input_data)
        
        if errors:
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_400_BAD_REQUEST,
            #     input_data=input_data,
            #     message="Validation failed",
            #     response_data=errors
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(message=errors)
        
        code =  random.randint(10000,99999)

        if input_data.get('user_id') is not None:
            
            user_has_setting = db_session_slave.query(UserHasSetting.sms_send).filter(UserHasSetting.user_id==input_data.get('user_id')).first()
            db_session_slave.commit()
            
            if user_has_setting.sms_send >= 5: 
                
                data = {
                    'data': None
                }
                
                # json_request = request_to_json(
                #     request=request,
                #     status=HTTP_200_OK,
                #     input_data=input_data,
                #     message="Sms limit reached.",
                #     response_data=data
                # )
                # send_message_to_sqs_job.delay(json_request)
                
                return generate_response(
                    data=data,
                    message="Sms limit reached.",
                    status=HTTP_200_OK
                )  
                
            else:
                send_sms_job.delay({
                    'code': code,
                    'phone_number': input_data.get('phone_number')
                })
                
                user_has_setting = db_session_master.query(UserHasSetting).filter(UserHasSetting.user_id==input_data.get('user_id')).first()
                user_has_setting.sms_send = user_has_setting.sms_send + 1
                db_session_master.commit()
        else: 
            send_sms_job.delay({
                'code': code,
                'phone_number': input_data.get('phone_number')
            })
        
        data = {
            'code': code,
        }
        
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=input_data,
        #     message="Sms send successfully.",
        #     response_data=data
        # )
        # send_message_to_sqs_job.delay(json_request)
            
        return generate_response(
            data= data,
            message="Sms send successfully.",
            status=HTTP_200_OK
        )
    except Exception as e:
        error_message =  str(e)
        
        json_request = request_to_json(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            input_data=input_data,
            message=error_message
        )
         
        send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )