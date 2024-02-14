from flask import Response
from flask_restful import Resource
from flask import request, make_response
from app.http.controllers.contacts.contact_controller import post, get, patch, delete


class ContactsResource(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = post(request, input_data)
        return make_response(response, status)
    
    @staticmethod
    def get() -> Response:
        
        """
        search users api
        """
        
        input_data = request.args
        response, status = get(request, input_data)
        return make_response(response, status)

class ContactResource(Resource):
    
    def patch(self,contact_id) -> Response:
        
        """
        search users api
        """
        
        input_data = request.get_json()
        response, status = patch(contact_id, input_data)
        return make_response(response, status)
    
    # @staticmethod
    def delete(self, contact_id) -> Response:

        """
        search users api
        """
        # input_data = request.get_json()
        response, status = delete(contact_id)
        return make_response(response, status)
    