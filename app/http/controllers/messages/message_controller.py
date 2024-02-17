from app.models.messages.message_model import Message, Survey
from app.utils.common import generate_response
from app.http.requests.messages.message_request import SendMessageSchema, ReactionToMessageSchema,MessageSchema
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from datetime import datetime
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from bson import ObjectId

@jwt_required()
def post(request, input_data):
    
    try:
        validator = SendMessageSchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors)
        
        message = Message (
            text = input_data.get('text'),
            responseToMsgId = input_data.get('response_to_msg_id') if   input_data.get('response_to_msg_id') else None,
            discussionId = input_data.get('discussion_id'),
            senderId = ObjectId(current_user._id),
            createdAt = datetime.utcnow().timestamp(),
            surveyId = input_data.get('survey_id') if   input_data.get('survey_id') else None
        )
        
        message.save()
            
        return generate_response(
            data=message, message="Message send successfully!", status=HTTP_201_CREATED
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def patch(message_id, input_data):
    
    try:
        validator = ReactionToMessageSchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors)
        
        message = Message.objects(
            _id = message_id
        ).first()
        
        if message is None: 
            return generate_response(
                message="Message not found!", status=HTTP_400_BAD_REQUEST
            )
            
        if input_data.get('action') == 'EMOJI_REACTION':
            reaction = {
                'userId': ObjectId(current_user._id),
                'emoji' : input_data.get('emoji')
            }
            message.reactions.append(reaction)
           
            message.save()
            
        return generate_response(
            data=message, message="Reaction send successfullly!", status=HTTP_201_CREATED
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def get(request, input_data):
    
    try:
        validator = MessageSchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors)
        
        messages = Message.objects(
            discussionId = input_data.get('discussion_id')
        )
        
            
        return generate_response(
            data=messages, message="", status=HTTP_200_OK
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )
