from flask import Response
from flask_restful import Resource
from flask import request, make_response
from app.http.controllers.users.user_controller import  create_user, search_user, patch
from flask_restful import reqparse

class UserResource(Resource): 
    @staticmethod
    def post() -> Response:
        """
        Create User Api.
        """
        
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)
    
    @staticmethod
    def get() -> Response:
        
        """
        search users api
        """
        
        input_data = request.args
        response, status = search_user(request, input_data)
        return make_response(response, status)
    
    @staticmethod
    def patch() -> Response:
        
        """
        search users api
        """
        input_data = request.get_json()
        response, status = patch(request, input_data)
        return make_response(response, status)