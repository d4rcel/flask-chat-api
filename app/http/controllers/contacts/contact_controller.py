from app.models.contacts.contact_model import Contact
from app.utils.common import generate_response
from app.http.requests.contacts.contact_request import CreateContactSchema, UpdateContactSchema
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from datetime import datetime
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from db import mongodb_client
from bson.objectid import ObjectId

@jwt_required()
def post(request, input_data):
    
    try:
        validator = CreateContactSchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors) 
         
        contact = Contact.objects.filter(
            mongodb_client.Q(
                user1Id=current_user._id,
                user2Id=input_data.get('user2Id'),
            )|
            mongodb_client.Q(
                user1Id=input_data.get('user2Id'),
                user2Id=current_user._id,
            )
        ).first()
        
        
        if contact : 
            if (contact.user1IdBlocked==False and contact.user2IdBlocked==False): 
                return generate_response(
                    data=[], message="You already is in this contact list", status=HTTP_200_OK
                )
                
            elif(contact.user1IdBlocked==True or contact.user2IdBlocked==True):
                
                pass
                
        contact = Contact(
            user1Id=ObjectId(current_user._id),
            user2Id=ObjectId(input_data.get('user2Id')),
            addedAt = datetime.utcnow().timestamp()
            # status = 'PENDING'
        )
        
        contact.save()
        
        return generate_response(
            data=contact, message="Contact Created", status=HTTP_201_CREATED
        )
       
        
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def get(request, input_data):
    
    data = []

    if input_data.get('status'):
        contacts = Contact.objects(
            # mongodb_client.Q(status=input_data.get('status')) |
            mongodb_client.Q(
                user1Id=current_user._id,
                user1IdBlocked=False,
                status=input_data.get('status')
            ) |
            mongodb_client.Q(
                user2Id=current_user._id,
                user2IdBlocked=False,
                status=input_data.get('status') 
            )
            # status=input_data.get('status')
        )
        
        for contact in contacts:
            data.append(contact.to_json())
    else:
        contacts = Contact.objects()
                
        for contact in contacts:
            data.append(contact.to_json())
    
    
    return generate_response(
        data=data, message="", status=HTTP_200_OK
    )
    
@jwt_required()
def patch(contact_id, input_data):
    
    try:
        validator = UpdateContactSchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors) 
        
        if input_data.get('action') == 'ANSWER_TO_REQUEST':
    
            contact = Contact.objects(
                _id=contact_id
            ).update(
                status  = input_data.get('status')
            )
            
        elif input_data.get('action') == 'BLOCKED_CONTACT':
           
            success = contact = Contact.objects(
                _id=contact_id,
                user1Id = current_user._id
            ).update(
                user2IdBlocked = input_data.get('isBlocked')
            )
                
            if success == 0:
                
                contact = Contact.objects(
                    _id=contact_id,
                    user2Id = current_user._id
                ).update(
                    user1IdBlocked = input_data.get('isBlocked')
                )
        
        return generate_response(
            data=contact, message="Update Succed", status=HTTP_200_OK
        )
    
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )
        
@jwt_required()
def delete(contact_id):
    
    try:
    
        contact = Contact.objects(
            _id=contact_id
        ).delete()
        
        return generate_response(
            data=contact, message="Contact deleted successfully.", status=HTTP_200_OK
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )