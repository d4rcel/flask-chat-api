from app.models.users.user_model import User
from app.utils.common import generate_response
from app.http.requests.login.login_request import LoginSchema,LogoutSchema
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED
from flask_jwt_extended import create_access_token
import datetime
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required,get_jwt, get_jwt_identity
from redis_client import jwt_redis_blocklist
from flask_bcrypt import check_password_hash
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
            return generate_response(message=errors)
       
        user = User.objects(email=input_data.get('email')).first()
        
        if user is None:
            
            message = "Unauthorized"
            
            return generate_response(message=message, status=HTTP_401_UNAUTHORIZED)
    
        if check_password_hash(user.password,input_data.get("password")): 
                            
            token = create_access_token(str(user._id),expires_delta=datetime.timedelta(days=365))
            
            data = {
                'token' : token,
                'user': user,
            }
            
            return generate_response(
                data=data, message="User login successfully", status=HTTP_200_OK
            )
            
        else:
            message = "Password is wrong"
           
            return generate_response(
                message=message, status=HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def logout(request):
    """
    It's use for logout a user
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
       
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
                
        message = f"{ttype.capitalize()} token successfully revoked"
        
        return generate_response(
            data={}, message=message, status=HTTP_200_OK
        )
    except Exception as e:
        
        error_message =  str(e)
        
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
        
        return generate_response(
            data={
                'token':access_token
            }, 
            message="",
            status=HTTP_200_OK
        )
        
    except Exception as e:
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )