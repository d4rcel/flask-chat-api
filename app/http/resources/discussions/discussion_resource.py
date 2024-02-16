from flask import Response
from flask_restful import Resource
from flask import request, make_response
from app.http.controllers.discussions.discussion_controller import post, get_discussion, get_discussions, patch, delete_discussion

class DiscussionsResource(Resource):
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
        response, status = get_discussions(request, input_data)
        return make_response(response, status)
    
class DiscussionResource(Resource):

    def get(self,discussion_id) -> Response:
        
        """
        search users api
        """
        
        # input_data = request.get_json()
        response, status = get_discussion(discussion_id)
        return make_response(response, status)
    
    def patch(self,discussion_id) -> Response:
        
        """
        search users api
        """
        
        input_data = request.get_json()
        response, status = patch(discussion_id, input_data)
        return make_response(response, status)
    
    def delete(self, discussion_id) -> Response:

        """
        search users api
        """
        # input_data = request.get_json()
        response, status = delete_discussion(discussion_id)
        return make_response(response, status)