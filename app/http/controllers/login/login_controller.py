from app.models.users.user_model import User, BlockedDevice
from app.utils.common import generate_response, request_to_json
from app.http.requests.login.login_request import LoginSchema,LogoutSchema
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_202_ACCEPTED, HTTP_500_INTERNAL_SERVER_ERROR
from flask_jwt_extended import create_access_token
import datetime
from db import db_session_slave
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required,get_jwt, get_jwt_identity
from redis_client import jwt_redis_blocklist
from flask_bcrypt import check_password_hash
from app.jobs.login.login_tasks import login_job, logout_job
from app.jobs.graylog.graylog_tasks import send_message_to_sqs_job
ACCESS_EXPIRES = datetime.timedelta(days=365)
    
def login(request, input_data):
    """
    It's use for login
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
        
        validator = LoginSchema()
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
        #     block_device = db_session_slave.query(BlockedDevice.id).filter(BlockedDevice.device_id==input_data.get('hardware_device_id')).first()
            
        #     if block_device:
        #         db_session_slave.commit()
                
        #         message = "You're try to connect with blocked device"
                
        #         json_request = request_to_json(
        #             request=request,
        #             status=HTTP_202_ACCEPTED,
        #             input_data=input_data,
        #             message=message
        #         )
        #         send_message_to_sqs_job.delay(json_request)
                
        #         return generate_response(message=message, status=HTTP_202_ACCEPTED)
        
        if input_data.get('type') == 'username': 
            get_user = db_session_slave.query(User).filter(User.username==input_data.get('username')).first()
        elif input_data.get('type') == 'email': 
            get_user = db_session_slave.query(User).filter(User.email==input_data.get('email')).first()

        db_session_slave.commit()
        
        if get_user is None:
            
            message = "User not found"
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_400_BAD_REQUEST,
            #     input_data=input_data,
            #     message=message
            # )
            # send_message_to_sqs_job.delay(json_request)
            return generate_response(message=message, status=HTTP_400_BAD_REQUEST)
        
        if get_user.deleted_at is not None:
            
            message = "User delete his account"
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_401_UNAUTHORIZED,
            #     input_data=input_data,
            #     message=message
            # )
            # send_message_to_sqs_job.delay(json_request)
            return generate_response(message=message, status=HTTP_401_UNAUTHORIZED)
    
        if get_user.is_suspended:
            
            message = "User is suspended"
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_401_UNAUTHORIZED,
            #     input_data=input_data,
            #     message=message
            # )
            # send_message_to_sqs_job.delay(json_request)
            return generate_response(message=message, status=HTTP_401_UNAUTHORIZED)
            
        # if hasattr(get_user,'blocked_at') and get_user.blocked_at is not None:
        #     return generate_response(message="User blocked", status=HTTP_401_UNAUTHORIZED)
    
          
        if check_password_hash(get_user.password,input_data.get("password")):        
                
            token = create_access_token(get_user.id,expires_delta=datetime.timedelta(days=365))
            
            data = {
                'token' : token,
                'user': get_user.to_json(),
            }
            
            # login_job.delay({
            #     'user_id': get_user.id,
            #     'device_id' : input_data.get('device_id'),
            #     'hardware_device_id' : input_data.get('hardware_device_id')
            # })
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message=None,
            #     response_data=data
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(
                data=data, message="User login successfully", status=HTTP_200_OK
            )
            
        else:
            message = "Password is wrong"
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_400_BAD_REQUEST,
            #     input_data=input_data,
            #     message=message
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(
                message=message, status=HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        
        error_message =  str(e)
        
        json_request = request_to_json(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            input_data=input_data,
            error_message=error_message
        )
         
        send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def logout(request,input_data):
    """
    It's use for logout a user
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
        validator = LogoutSchema()
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
        
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        
        user_id = current_user.get('id')
        
        logout_job.delay({
            'user_id': user_id,
            'device_id' : input_data.get('device_id'),
            'hardware_device_id' : input_data.get('hardware_device_id')
        })
        
        message = f"{ttype.capitalize()} token successfully revoked"
        
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=input_data,
        #     message=message
        # )
        # send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            data={}, message=message, status=HTTP_200_OK
        )
    except Exception as e:
        
        error_message =  str(e)
        
        json_request = request_to_json(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            input_data=None,
            error_message=error_message
        )
         
        send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def refresh(request):
    """
    It's use for refresh authentificate user token
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
        
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=None,
        #     message=None
        # )
        # send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            data={
                'token':access_token
            }, 
            message="",
            status=HTTP_200_OK
        )
        
    except Exception as e:
        error_message =  str(e)
        
        json_request = request_to_json(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            input_data=None,
            error_message=error_message
        )
         
        send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )