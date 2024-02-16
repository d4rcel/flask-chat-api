from app.models.discussions.discussion_model import Discussion, Member
from app.utils.common import generate_response
from app.http.requests.discussions.discussion_request import CreateGroupDiscussionSchema, UpdateDiscussionSchema, DiscussionSchema
from app.utils.http_code import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from datetime import datetime
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from db import mongodb_client
from bson import ObjectId

@jwt_required()
def post(request, input_data):
    
    try:
        validator = CreateGroupDiscussionSchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors)
        
        member_ids = [item['userId'] for item in input_data.get('members')]
        
        if str(current_user._id) not in member_ids:
            member_ids.append(str(current_user._id))
        
        discussion = None
        
        if input_data.get('tag') == 'PRIVATE':
            
            if len(member_ids)  != 2:
                return generate_response(
                    data=discussion, message="Total member for private discussion should not be exced 2.", status=HTTP_200_OK
                )
            discussion = Discussion.objects(members__all=[{'userId': member_ids[0]}, {'userId': member_ids[1] }]).first()
            
        
        if discussion:
            
            return generate_response(
                data=discussion, message="Discussion already created", status=HTTP_200_OK
            )
                        
        discussion = Discussion(
            name = input_data.get('name') if input_data.get('tag') == 'GROUP' else None,
            tag = input_data.get('tag'),
            createdBy =  ObjectId(current_user._id),
            updatedAt = datetime.utcnow().timestamp(),
            description = input_data.get('description') if input_data.get('tag') == 'GROUPE' else None,
            members = []
        )
                
        for member in member_ids: 
                        
            member = {
                'userId': ObjectId(member),
                'isPined' : False,
                'isMuted' : False,
                'isAdmin' : member==str(current_user._id) and input_data.get('tag') == 'GROUP',
                'isArchived' : False,
                'addedAt': datetime.utcnow().timestamp()
            }
            
            discussion.members.append(
                member
            )
        
        discussion.save()
            
        return generate_response(
            data=discussion, message="Contact Created", status=HTTP_201_CREATED
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def get_discussions(request, input_data):
    
    try:
        validator = DiscussionSchema()
        errors = validator.validate(input_data)
            
        if errors:
            return generate_response(message=errors) 
        
        filters = {
            'userId': current_user._id
        }
        
        if input_data.get('is_pined') and input_data.get('is_archived'):
            
            return generate_response(
                data={}, message="You can't combine this two route", status=HTTP_400_BAD_REQUEST
            )
    
        if input_data.get('is_pined'):
            if input_data.get('is_pined') in [1, 'true', 'True']:
                filters['isPined'] = True
            else:
                filters['isPined'] = False
            
        if input_data.get('is_archived') :
            if input_data.get('is_archived') in [1, 'true', 'True']:
                filters['isArchived'] = True
            else:
                filters['isArchived'] = False
    
        discussions = Discussion.objects(
            members__elemMatch=filters
        )
    
        return generate_response(
            data=discussions, message="", status=HTTP_200_OK
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def get_discussion(discussion_id):
    
    try:
        discussion = Discussion.objects(_id=discussion_id)
        
        return generate_response(
            data=discussion, message="", status=HTTP_200_OK
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def delete_discussion(discussion_id):
    try:
        discussion = Discussion.objects(
            _id=discussion_id
        ).delete()
        
        return generate_response(
            data=discussion, message="", status=HTTP_200_OK
        )
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )

@jwt_required()
def patch(discussion_id, input_data):
    
    try:
        validator = UpdateDiscussionSchema()
        errors = validator.validate(input_data)
        
        if errors:
            return generate_response(message=errors)
        
        discussion = Discussion.objects(
            _id = discussion_id,
            tag = 'GROUP'
        ).first()
        
        if discussion is None:
            return generate_response(
                data={}, message="You can't perform this discussion", status=HTTP_400_BAD_REQUEST
            )
            
        if input_data.get('action') == 'ADD_USERS_GROUP':
            
            if Discussion.objects(_id = discussion_id, members__userId = current_user._id,members__isAdmin = True).first() is None:
                
                return generate_response(
                    data={}, message="You are not authorized to perform this action", status=HTTP_400_BAD_REQUEST
                )
            
            for user in input_data.get('add_users'): 
                
                found = Discussion.objects(
                    _id = discussion_id,
                    members__elemMatch =  {'userId' : ObjectId(user)}
                ).first()
                
                                
                if found is None:
            
                    member = {
                        'userId': ObjectId(user),
                        'isPined' : False,
                        'isMuted' : False,
                        'isAdmin' : False,
                        'isArchived' : False,
                        'addedAt': datetime.utcnow().timestamp()
                    }
                    
                    discussion.members.append(
                        member
                    )
                
            discussion.save()
            
            return generate_response(
                data=discussion, message="Member added successfully!", status=HTTP_201_CREATED
            )
            
        if input_data.get('action') == 'UPDATE_GROUP_INFO':
            
            discussion = Discussion.objects(
                _id = discussion_id,
            ).update(
                name = input_data.get('name'),
                description = input_data.get('description'),
            )
        
            return generate_response(
                data=discussion, message="Group detail updated successfully!", status=HTTP_200_OK
            )
            
        if input_data.get('action') == 'ARCHIVED':
            
            if input_data.get('is_archived') is None: 
                
                return generate_response(
                    message="is_archived is missed", status=HTTP_201_CREATED
                )   
            # print(input_data.get('is_archived'))
            # print(discussion_id)      
                    
            discussion = Discussion.objects(
                _id = discussion_id,
                # members__elemMatch= {'userId': current_user._id}
                members__userId = current_user._id
            ).first()
            # .update(
            #     set__members__S__isArchived=input_data.get('is_archived')
            # )
            
            
            for member in discussion.members:
                if member.get('userId') == ObjectId(current_user._id):
                    member['isArchived'] = input_data.get('is_archived')
                    break
            
            discussion.save()  
                  
            return generate_response(
                data=discussion, message="Discussion archived successfully", status=HTTP_201_CREATED
            )
        
        if input_data.get('action') == 'PINED':    
            
            if input_data.get('is_pined') is None: 
                
                return generate_response(
                    message="is pined is missed", status=HTTP_201_CREATED
                )   
            
            discussion = Discussion.objects(
                _id = discussion_id,
                members__userId = current_user._id
            ).first()
            
            for member in discussion.members:
                if member.get('userId') == ObjectId(current_user._id):
                    member['isPined'] = input_data.get('is_pined')
                    break
            
            discussion.save()  
                  
            return generate_response(
                data=discussion, message="Discussion pined or unpinded successfully", status=HTTP_201_CREATED
            )
            
        if input_data.get('action') == 'MUTED':    
            
            if input_data.get('is_muted') is None: 
                
                return generate_response(
                    message="is muted is missed", status=HTTP_201_CREATED
                )   
            
            discussion = Discussion.objects(
                _id = discussion_id,
                members__userId = current_user._id
            ).first()
                
            for member in discussion.members:
                if member.get('userId') == ObjectId(current_user._id):
                    member['isMuted'] = input_data.get('is_muted')
                    break
            
            discussion.save()  
                  
            return generate_response(
                data=discussion, message="Discussion pined or unpinded successfully", status=HTTP_200_OK
            )
                    
        if input_data.get('action') == 'REMOVE_USERS_GROUP':    
            
            if input_data.get('remove_users') is None: 
                
                return generate_response(
                    message="Remove users is missed", status=HTTP_400_BAD_REQUEST
                )
            
            if Discussion.objects(_id = discussion_id, members__userId = current_user._id,members__isAdmin = True).first() is None:
                
                return generate_response(
                    data={}, message="You are not authorized to perform this action", status=HTTP_400_BAD_REQUEST
                )
                    
            members = []
            
            for  member in discussion.members:
                
                if str(member.get('userId')) not in input_data.get('remove_users'):
                    # if member.get('isAdmin') == True:
                    members.append(member)            

            discussion.members = members

            discussion.save() 
             
            return generate_response(
                data=discussion, message="User remove successfully", status=HTTP_200_OK
            )
            
        if input_data.get('action') == 'LEAVE_GROUP':    
            
            
            if Discussion.objects(_id = discussion_id, members__userId = current_user._id).first() is None:
                
                return generate_response(
                    data={}, message="You are not authorized to perform this action", status=HTTP_400_BAD_REQUEST
                )
                    
            members = []
            
            for  member in discussion.members:
                
                if member.get('userId') != ObjectId(current_user._id):
                    members.append(member)            

            discussion.members = members

            discussion.save() 
             
            return generate_response(
                data=discussion, message="User remove successfully", status=HTTP_200_OK
            )
            
        return generate_response(
            data={}, message="", status=HTTP_201_CREATED
        )
        
    except Exception as e:
        
        error_message =  str(e)
        
        return generate_response(
            message=error_message, status=HTTP_200_OK
        )