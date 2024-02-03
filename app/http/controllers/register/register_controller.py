from app.utils.common import generate_response, request_to_json
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_500_INTERNAL_SERVER_ERROR
from db import db_session_slave, db_session_master
from app.http.requests.register.register_request import UsernameSchema, EmailSchema, RegisterSchema
from app.models.users.user_model import User, BlockedDevice
from flask_jwt_extended import create_access_token
import datetime
from redis_client import username_redis_client, mail_redis_client
from app.jobs.graylog.graylog_tasks import send_message_to_sqs_job

def check_username(request, input_data):
    """
    It check if username it's available for register
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    
    try:
        validator = UsernameSchema()
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
        
        # if input_data.get('hardware_device_id'):
            
        #     block_device = db_session_slave.query(BlockedDevice.id)\
        #         .filter(BlockedDevice.device_id==input_data.get('hardware_device_id'))\
        #         .first()
        #     db_session_slave.commit()
            
        #     if block_device:
                
        #         message = "You're try to connect with blocked device"
                
        #         json_request = request_to_json(
        #             request=request,
        #             status=HTTP_202_ACCEPTED,
        #             input_data=input_data,
        #             message=message
        #         )
        #         send_message_to_sqs_job.delay(json_request)
                
        #         return generate_response(message=message, status=HTTP_202_ACCEPTED)
        get_user = db_session_slave.query(User.id).filter(User.username==input_data.get('username')).first()
        # get_user = username_redis_client.get('prod_api_database_username_'+str(input_data.get('username')))
        db_session_slave.commit()
        
        if get_user is None :
            
            message="Username is available"
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message=message
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(data=input_data,message=message, status=HTTP_200_OK)
        else:
            
            message='Username is already use'
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message=message
            # )
            # send_message_to_sqs_job.delay(json_request)
            return generate_response(data=input_data,message=message,status=HTTP_200_OK)
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
    
def check_email(request, input_data):
    """
    It check if email it's available for register
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
        validator = EmailSchema()
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

        get_user = db_session_slave.query(User.id).filter(User.email==input_data.get('email')).first()
        # get_user = mail_redis_client.get('prod_api_database_email_'+str(input_data.get('email')))
        db_session_slave.commit()
        
        if get_user is None:
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message='Email is available'
            # )
            # send_message_to_sqs_job.delay(json_request)
            return generate_response(data=input_data,message='Email is available', status=HTTP_200_OK)
        else:
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message='Email is already use'
            # )
            # send_message_to_sqs_job.delay(json_request)
            return generate_response(data=input_data,message='Email is already use',status=HTTP_200_OK)
        
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
     
def register(request, input_data):
    """
    It use for register a new user
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
        
        create_validation_schema = RegisterSchema()
        errors = create_validation_schema.validate(input_data)
        
        if errors:
                            
            return generate_response(message=errors)
    
        # check_user = db_session_master.query(User.id).filter(
        #     or_(
        #         User.username==input_data.get('username'),
        #         User.email==input_data.get('email')
        #     )
        # ).first()

        # db_session_slave.commit()
        # if check_user is None:
        #     
        new_user = User(**input_data)  
        
        user = new_user.to_json()
                    
        return generate_response(
            data=user, message="User Created", status=HTTP_201_CREATED
        )
            
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )