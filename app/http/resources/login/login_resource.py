from flask import Response
from flask_restful import Resource
from flask import request, make_response
from app.http.controllers.login.login_controller import login, logout, refresh


class LoginResource(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = login(request, input_data)
        return make_response(response, status)
    
class LogoutResource(Resource):
    @staticmethod
    def post()  ->  Response:
        response , status = logout(request)
        return make_response(response, status)
    
class RefreshTokenResource(Resource):
    @staticmethod
    def post()  -> Response:
        response , status = refresh(request)
        return make_response(response, status)

