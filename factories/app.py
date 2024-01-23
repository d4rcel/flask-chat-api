from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from db import mysql_mongodb_client
from app.http.resources.login.login_resource import LoginResource, LogoutResource, RefreshTokenResource
from app.http.resources.register.register_resource import CheckUsernameResource, CheckEmailResource, RegisterResource
from app.http.resources.sms.sms_resource import SendSMSResource
from app.http.resources.users.user_resource import SendResetPasswordCodeResource,CheckResetPasswordCodeResource, ResetPasswordResource,\
    SendVerifyEmailCodeResource,VerifyEmailResource, UpdateNoticifactionDeviceIdResource, UpdateUserHadwareDeviceIdResource
from app.http.resources.home.home_resource import HomeResource
from app.exceptions.handler import handle_404_error, handle_500_error
from app.models.users.user_model import User
from redis_client import jwt_redis_blocklist
from datetime import timedelta
from flask import jsonify
from app.utils.http_code import HTTP_401_UNAUTHORIZED
from werkzeug.exceptions import NotFound
from healthcheck import HealthCheck, EnvironmentDump

def create_app() -> Flask:

    app = Flask(__name__, template_folder='../templates')
    config = Config()
    
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # Setup the Flask-JWT-Extended extension
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['JWT_ALGO'] = config.JWT_ALGO
    app.config['JWT_ACCESS_TOKEN_EXPIRES']  =   timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] =   timedelta(days=365)
    
    #ELASTICSEARCH
    app.config['ELASTICSEARCH_HOST'] = Config.ELASTICSEARCH_HOST
    
    health = HealthCheck()
    
    # health.add_check()
    envdump = EnvironmentDump()

    jwt = JWTManager(app)

    api = Api(app=app)


    mysql_mongodb_client.init_app(app, Config.MYSQL_MONGO_URI)
        
    # Register a callback function that takes whatever object is passed in as the
    # identity when creating JWTs and converts it to a JSON serializable format.
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        
        user = mysql_mongodb_client.db.users.find_one({'id': identity})
    
        user = {
            'id' : user.get('id')
        }
        
        return user
        # user = db_session_slave.query(User).filter(User.id==identity).one_or_none()
        # db_session_slave.commit()
        # return user
    
    @jwt.invalid_token_loader
    def invalid_token_loader(callback):
        return jsonify(msg="Unauthorized"), HTTP_401_UNAUTHORIZED
    
    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    # Add a flask route to expose information
    app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())

    app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())

    api.add_resource(HomeResource, '/')
    
    api.add_resource(LoginResource, '/api/login')

    api.add_resource(RegisterResource,'/api/register')

    api.add_resource(CheckUsernameResource, '/api/check/username')

    api.add_resource(CheckEmailResource,'/api/check/email')
    
    api.add_resource(LogoutResource,'/api/logout')
    
    api.add_resource(RefreshTokenResource,'/api/refresh')
    
    api.add_resource(SendSMSResource,'/api/send/sms')
    
    api.add_resource(SendResetPasswordCodeResource,'/api/send/reset/password/code')

    api.add_resource(CheckResetPasswordCodeResource,'/api/check/reset/password/code')
    
    api.add_resource(ResetPasswordResource,'/api/reset/password')
    
    api.add_resource(SendVerifyEmailCodeResource,'/api/send/verify/email/code')

    api.add_resource(VerifyEmailResource,'/api/verify/email')

    api.add_resource(UpdateNoticifactionDeviceIdResource,'/api/update/notification/device/id')

    api.add_resource(UpdateUserHadwareDeviceIdResource,'/api/update/user/hardaware/device/id')

    @app.errorhandler(404)
    def handle(e):
        return handle_404_error(e)

    @app.errorhandler(500)
    def handle(e):
        return handle_500_error(e)
    
    @app.errorhandler(405)
    def handle(e):
        return handle_404_error(e)
    
    return app
