from flask import Response
from flask_restful import Resource
from flask import request, make_response
from app.http.controllers.surveys.survey_controller import post, patch, get

class SurveysResource(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = post(request, input_data)
        return make_response(response, status)


class SurveyResource(Resource):
    
    def patch(self, survey_id) -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = request.get_json()
        response, status = patch(survey_id, input_data)
        return make_response(response, status)

    def get(self, survey_id) -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        # input_data = request.get_json()
        response, status = get(survey_id)
        return make_response(response, status)