from app.models.messages.message_model import Survey
from app.utils.common import generate_response
from app.http.requests.surveys.survey_request import CreateSurveySchema, UpdateSurveySchema
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from datetime import datetime
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from bson import ObjectId
from app.utils.common import generate_random_string

@jwt_required()
def post(request, input_data):
    
    try:
        validator = CreateSurveySchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors)
        
        survey = Survey (
            question = input_data.get('question'),
            discussionId = input_data.get('discussion_id'),
            creatorId = ObjectId(current_user._id),
            createdAt = datetime.utcnow().timestamp(),
            endedAt = datetime.utcnow().timestamp(),
            options = []
        )
        
        for response in input_data.get('options'):
            
            option = {
                'id': generate_random_string(5),
                'response' :  response,
                'votes': []
            }
            survey.options.append(option)
        
        survey.save()
            
        return generate_response(
            data=survey, message="Survey created successfully!", status=HTTP_201_CREATED
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def get(survey_id):
    
    try:
        
        surveys = Survey.objects(
            _id = survey_id,
        )
            
        return generate_response(
            data=surveys, message="", status=HTTP_201_CREATED
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )
        
@jwt_required()
def patch(survey_id, input_data):
    
    # try:
        validator = UpdateSurveySchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors)
        
        survey = Survey.objects(
            _id = survey_id,
            options__elemMatch =  {'id' : input_data.get('option_id')}
        ).first()
        
        if survey is None: 
            return generate_response(
                message="Survey not found!", status=HTTP_400_BAD_REQUEST
            )
        
        options = []

        for option in survey.options:
            print(option.get('votes'))
            votes = []

            if option.get('id') == input_data.get('option_id'):
                if input_data.get('is_selected')==True and ObjectId(current_user._id) not in option.get('votes'):
                    option['votes'].append(ObjectId(current_user._id))
                elif  input_data.get('is_selected')==False and ObjectId(current_user._id) in option.get('votes'):
                    for user_id in option.get('votes'):
                        if str(user_id) != str(current_user._id):
                            votes.append(ObjectId(user_id))
                      
                    option['votes'] = votes
                options.append(option)
            else:
                options.append(option)
        
        survey.save()
            
        return generate_response(
            data=survey, message="Reaction send successfullly!", status=HTTP_201_CREATED
        )
    # except Exception as e:
        
    #     error_message =  str(e)
        
    #     return generate_response(
    #         message=error_message, status=HTTP_200_OK
    #     )