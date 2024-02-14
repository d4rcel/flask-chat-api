from app.models.discussions.discussion_model import Discussion, Member
from app.utils.common import generate_response
from app.http.requests.discussions.discussion_request import CreateDiscussionSchema
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from datetime import datetime
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from db import mongodb_client
from bson.objectid import ObjectId

def post(request, input_data):
    
    try:
        validator = CreateDiscussionSchema()
        errors = validator.validate(input_data)
        
        member_ids = [item['id'] for item in input_data.get('members')]
        
        if input_data.get('tag') == 'PRIVATE': 
            find = Discussion.objects(roles__in=[member_ids])
            
            
        discussion = Discussion(
            name = input_data
        )
        
        
        return generate_response(
            data={}, message="Contact Created", status=HTTP_201_CREATED
        )
       
    
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )
    