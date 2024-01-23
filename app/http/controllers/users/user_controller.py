from app.models.users.user_model import User, UserHasDevice, Device
from app.utils.common import generate_response, request_to_json
from app.http.requests.users.user_request import SendResetPasswordCodeSchema,ResetPasswordSchema,\
    CheckResetPasswordCodeSchema,VerifyEmailCodeSchema, UpdateDeviceIdInputSchema, UpdateHadwareDeviceIdInputSchema
from db import db_session_master, db_session_slave
from app.utils.http_code import HTTP_200_OK, HTTP_201_CREATED,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
import random
from app.jobs.users.user_tasks import send_reset_password_code_job, send_verify_email_code_job
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from datetime import datetime 
from app.jobs.graylog.graylog_tasks import send_message_to_sqs_job

def send_reset_password_code(request, input_data):
    """
    It's use for send reset password code
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
        
        validator = SendResetPasswordCodeSchema()
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
        
        if input_data.get('phone_number') is not None:
            user = db_session_slave.query(User.id, User.username).filter(User.phone_number==input_data.get('phone_number')).first()
        elif input_data.get('email') is not None:
            user = db_session_slave.query(User.id,User.username).filter(User.email==input_data.get('email')).first()
        db_session_slave.commit()
    
        if user is None:
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message="WRONG DATA",
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(
                message="WRONG DATA",
                status=HTTP_200_OK
            )
                
        else:
            code =  random.randint(10000,99999)
            
            db_session_master.query(User).filter(User.id==user.id).update({
                'reset_password_code' : code
            })
            db_session_master.commit()
            
            send_reset_password_code_job.delay({
                'username': user.username,
                'phone_number': input_data.get('phone_number'),
                'email': input_data.get('email'),
                'code': code
            })
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message="The reset code is send successfully",
            #     response_data={
            #         'code': code
            #     }
            # )
            # send_message_to_sqs_job.delay(json_request)
        
            return generate_response(
                data=code,
                message="The reset code is send successfully",
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
        
def check_reset_password_code(request, input_data):
    
    try:
        
        validator = CheckResetPasswordCodeSchema()
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
        
        if input_data.get('phone_number') is not None:
            user = db_session_slave.query(User.id).filter(User.phone_number==input_data.get('phone_number'),User.reset_password_code==input_data.get('code')).first()
        elif input_data.get('email') is not None:
            user = db_session_slave.query(User.id).filter(User.email==input_data.get('email'),User.reset_password_code==input_data.get('code')).first()
            
        db_session_slave.commit()
        
        if user is None:
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message="WRONG CODE.",
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(
                message="WRONG CODE",
                status=HTTP_200_OK
            )
            
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=input_data,
        #     message="GOOD CODE.",
        # )
        # send_message_to_sqs_job.delay(json_request) 
        
        return generate_response(
            message="GOOD CODE",
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
    
def reset_password(request, input_data):
    try:
        
        """
        It's use for login
        :param request: The request object
        :param input_data: This is the data that is passed to the function
        :return: A response object
        """
        
        validator = ResetPasswordSchema()
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
        
        if input_data.get('phone_number') is not None:
            user = db_session_slave.query(User.id)\
                .filter(
                    User.phone_number==input_data.get('phone_number'),
                    User.reset_password_code==input_data.get('code')
                ).first()
        elif input_data.get('email') is not None:
            user = db_session_slave.query(User)\
                .filter(
                    User.email==input_data.get('email'),
                    User.reset_password_code==input_data.get('code')
                ).first()
        db_session_slave.commit()
    
        if user is None:
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message="WRONG CODE."
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(
                data= None,
                message="WRONG CODE",
                status=HTTP_200_OK
            )
        
        db_session_master.query(User).filter(User.id==user.id).update({
            'password' : generate_password_hash(input_data.get('password')).decode("utf8"),
            'reset_password_code' : None
        })
        db_session_master.commit()
        
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_201_CREATED,
        #     input_data=input_data,
        #     message="The reset code is reset successfully.",
        # )
        # send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            data= {
                'data': input_data,
            },
            message="The reset code is reset successfully",
            status=HTTP_201_CREATED
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

@jwt_required()
def send_verify_email_code(request):
    try:
        
        code = random.randint(10000,99999)
        
        user_id = current_user.get('id')
        user =  db_session_master.query(User.id, User.email, User.email).filter(User.id==user_id).first()
        db_session_master.query(User).filter(User.id==user.id).update({
            'verify_email_code': code
        })
        db_session_master.commit()
        
        send_verify_email_code_job.delay({
            'username': user.username,
            'email': user.email,
            'code':  code
        })
        
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=None,
        #     message="Success."
        # )
        # send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            data=code,
            message="Success",
            status=HTTP_200_OK
        )
    except Exception as e:
        error_message =  str(e)
        
        json_request = request_to_json(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            input_data=None,
            message=error_message
        )
         
        send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def verify_email(request, input_data):
    
    try:
        
        validator = VerifyEmailCodeSchema()
        errors = validator.validate(input_data)
        
        if errors:
            
            json_request = request_to_json(
                request=request,
                status=HTTP_400_BAD_REQUEST,
                input_data=input_data,
                message="Validation failed",
                response_data=errors
            )
            send_message_to_sqs_job.delay(json_request)
            
            return generate_response(message=errors)
        
        user_id = current_user.get('id')
        user = db_session_slave.query(User.id)\
            .filter(
                User.id==user_id,
                User.verify_email_code ==input_data.get('code')
            ).first()
        db_session_slave.commit()

        if user is None:
            
            # json_request = request_to_json(
            #     request=request,
            #     status=HTTP_200_OK,
            #     input_data=input_data,
            #     message="WRONG CODE.",
            # )
            # send_message_to_sqs_job.delay(json_request)
            
            return generate_response(
                message="WRONG CODE",
                status=HTTP_200_OK
            )
        
        user_id = current_user.get('id')
        user = db_session_master.query(User).filter(User.id==user_id).update({
            'verify_email_code': None,
            'email_verified_at': datetime.utcnow().date().strftime('%Y-%m-%d')
        })
        db_session_master.commit()
        
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=input_data,
        #     message="Success."
        # )
        # send_message_to_sqs_job.delay(json_request)
        
        return generate_response(
            message="Success",
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

@jwt_required()
def update_notification_device_id(request, input_data):
    try:
        
        validator = UpdateDeviceIdInputSchema()
        errors = validator.validate(input_data)
        
        user_id = current_user.get('id')
        
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
        
        try:
            db_session_master.query(UserHasDevice).filter(
                UserHasDevice.device_id==input_data.get('device_id')
            ).delete()
            user_has_device = UserHasDevice(
                user_id, 
                input_data.get('device_id')
            )
            db_session_master.add(user_has_device)
            db_session_master.commit()
        except:
            db_session_master.rollback()
       
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=input_data,
        #     message="Updated Successfully."
        # )
        # send_message_to_sqs_job.delay(json_request)
            
        return generate_response(
            data=input_data,
            message="Updated Successfully",
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
    
@jwt_required()
def update_user_hardware_device_id(request, input_data):
    try:
        
        validator = UpdateHadwareDeviceIdInputSchema()
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
        
        try:
            db_session_master.query(Device)\
                .filter(
                    Device.device_id==input_data.get('hardware_device_id')
                ).delete()
            device = Device(user_id=input_data.get('user_id'),device_id=input_data.get('hardware_device_id'))
            db_session_master.add(device)
            db_session_master.commit()
        except:
            db_session_master.rollback()
        
        # json_request = request_to_json(
        #     request=request,
        #     status=HTTP_200_OK,
        #     input_data=input_data,
        #     message="Updated Successfully."
        # )
        # send_message_to_sqs_job.delay(json_request)
            
        return generate_response(
            data=input_data,
            message="Updated Successfully",
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