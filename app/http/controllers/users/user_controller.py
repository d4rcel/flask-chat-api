from app.models.users.user_model import User
from app.utils.common import generate_response, request_to_json
from app.http.requests.users.user_request import CreateUserSchema, SearchUserInputSchema, EditUserSchema
from db import mongodb_client
from app.utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
import random
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

def create_user(request, input_data):
    """
    It use for register a new user
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    try:
        
        create_validation_schema = CreateUserSchema()
        errors = create_validation_schema.validate(input_data)
        
        if errors:     
            return generate_response(message=errors)
        
        if User.objects(email=input_data.get('email')).first():        
            message = "Email already exists"
            return generate_response(message=message, status=HTTP_400_BAD_REQUEST)
        
        
        user = User(
            firstname = input_data.get('firstname'),
            lastname = input_data.get('lastname'),
            email = input_data.get('email'),
            password = generate_password_hash(input_data.get('password')).decode("utf8"),
            photoUrl = None,
            status = None
        ).save()
                            
        return generate_response(
            data=user, message="User Created", status=HTTP_201_CREATED
        )
            
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )
    
@jwt_required()
def edit_user(request,input_data):
    
    valiator = EditUserSchema()
    errors = valiator.validate(input_data)
    
    if errors:
        return generate_response(message=errors) 
        
    user = User.objects(email=input_data.get('email')).first()
    
    if user and user._id != current_user._id:
        
        message = "Email already exists"
        return generate_response(message=message, status=HTTP_400_BAD_REQUEST)
        
    User.objects(email=current_user.email).update(
        firstname = input_data.get('firstname') if  input_data.get('firstname')  else current_user.firstname,
        lastname =input_data.get('lastname') if input_data.get('lastname') else current_user.lastname,
        email = input_data.get('email') if input_data.get('email') else current_user.email,
        photoUrl = None,
        status = input_data.get('status') if input_data.get('status') else current_user.status
    )

    return generate_response(
        data={}, message="Update Succed", status=HTTP_200_OK
    )
    
@jwt_required()
def search_user(request,input_data):
    
    valiator = SearchUserInputSchema()
    errors = valiator.validate(input_data)
    
    if errors:
        return generate_response(message=errors) 
    
    if input_data.get('search') :
        users = User.objects.filter(
            mongodb_client.Q(firstname__icontains=input_data.get('search')) |
            mongodb_client.Q(lastname__icontains=input_data.get('search')) |
            mongodb_client.Q(email__icontains=input_data.get('search'))
        )
    else:
        users = User.objects()
        
    return generate_response(
        data=users, message="", status=HTTP_200_OK
    )