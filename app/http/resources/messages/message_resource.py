from flask import Response
from flask_restful import Resource
from flask import request, make_response
from app.http.controllers.messages.message_controller import post, patch, get

class MessagesResource(Resource):
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
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.args
        response, status = get(request, input_data)
        return make_response(response, status)
    

class MessageResource(Resource):
    
    def patch(self, message_id) -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = patch(message_id, input_data)
        return make_response(response, status)