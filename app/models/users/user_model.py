"""User model."""
import datetime
from db import db
from flask_bcrypt import generate_password_hash
from config import Config

# The User class is a data model for user accounts
class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True, index=True, autoincrement=True)
    last_name = db.Column(db.String(255),index=True, nullable=True)
    first_name = db.Column(db.String(255), index=True, nullable=True)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), index=True, nullable=True, unique=True)
    path = db.Column(db.String(255), nullable=True)
    cover_photo_url = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), index=True, nullable=False)
    phone_number = db.Column(db.String(255), index=True, unique=True, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    reset_password_code = db.Column(db.String(255), nullable=True)
    verify_email_code = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    profession = db.Column(db.String(255), nullable=True)
    thumbnail = db.Column(db.String(255), nullable=True)
    is_private = db.Column(db.String(255), nullable=True)
    is_suspended = db.Column(db.String(255), default=False)
    certification_status = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, **kwargs):
        """
        The function takes in a dictionary of keyword arguments and assigns the values to the class
        attributes
        """
        self.last_name = kwargs.get("last_name")
        self.first_name = kwargs.get("first_name")
        self.birth_date = kwargs.get("birth_date")
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.phone_number = kwargs.get("phone_number")
        self.status = 'A'
        self.is_private = False
        self.password = generate_password_hash(kwargs.get('password')).decode("utf8")

    def to_json(self):
        
        if self.path is not None:
            aws_file_path_uuid = self.path.split('.')[0]
            photo_url = Config.MEDIA_CDN_URL+self.path
            file_208_208 = Config.THUNBNAIL_CDN_URL+aws_file_path_uuid+'_208x208.jpg'
        else:
            photo_url = None
            file_208_208 = None
            
        if self.cover_photo_url is not None:
            aws_file_cover_uuid = self.cover_photo_url.split('.')[0]
            cover_photo_url  = Config.MEDIA_CDN_URL+self.cover_photo_url
            thunbnail_cover_url =  Config.THUNBNAIL_CDN_URL+aws_file_cover_uuid+'_860x360.jpg'
        else:
            cover_photo_url = None
            thunbnail_cover_url = None
        
        if type(self.birth_date) == str:
            birth_date = self.birth_date
        else:
            birth_date = self.birth_date.strftime('%Y-%m-%d %H:%M:%S')
            
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthdate': birth_date,
            'email': self.email,
            'path': self.path,
            'photo_url': photo_url,
            'file_208_x_208':file_208_208,
            'username':  self.username,
            'phone_number': self.phone_number,
            'cover_photo_url': cover_photo_url,
            'file_cover_url':thunbnail_cover_url,
            'gender' : self.gender,
            'reset_password_code' : self.reset_password_code,
            'verify_email_code' : self.verify_email_code,
            'status' :  self.status,
            'profession' : self.profession,
            'thumbnail' :  self.thumbnail,
            'is_private' : self.is_private,
            'certification_status' :  self.certification_status,
            'created_at' : self.created_at.strftime('%Y-%m-%d %H:%M:%S')          
        }

    def __repr__(self):
        """
        The __repr__ function is used to return a string representation of the object
        :return: The username of the user.
        """
        return "<User {}>".format(self.username)

class UserHasDevice(db.Model):
    """ User has device model class"""
     
    __tablename__ = "user_has_devices"
    id = db.Column(db.BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey(User.id), index=True)
    device_id = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, user_id: int, device_id: int):
        self.user_id = user_id
        self.device_id = device_id
        
class Device(db.Model):
    """ Device model class"""
     
    __tablename__ = "devices"
    id = db.Column(db.BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True, index=True)
    device_id = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, user_id: int, device_id: int):
        self.user_id = user_id
        self.device_id = device_id
        
class BlockedDevice(db.Model):
    """ Device model class"""
     
    __tablename__ = "blocked_devices"
    id = db.Column(db.BigInteger, primary_key=True, index=True, autoincrement=True)
    device_id = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, user_id: int, device_id: int):
        self.device_id = device_id
        
class UserHasSetting(db.Model):
    """User Setting model class"""

    __tablename__ = "user_has_settings"
    id = db.Column(db.BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True, index=True)
    is_private = db.Column(db.Boolean, default=False)
    is_certified = db.Column(db.Boolean, default=False)
    comment_on_story = db.Column(db.Boolean, default=True)
    online_status = db.Column(db.Boolean,default=True)
    language = db.Column(db.String(255),default="french")
    certification_status = db.Column(db.String(255))
    story_multiplier_view = db.Column(db.Float,default=1.0)
    is_online = db.Column(db.Boolean,default=False)
    last_online_date = db.Column(db.TIMESTAMP)
    sms_send = db.Column(db.Integer,default=0)
    last_time_sms_send = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)


    def __init__(self, user_id):
        """
        The function takes in a dictionary of keyword arguments and assigns the values to the class
        attributes
        """
        self.user_id = user_id,
    
    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sms_send': self.sms_send
            # 'first_name': self.first_name,
            # 'last_name': self.last_name,
        }

    def __repr__(self):
        """
        The __repr__ function is used to return a string representation of the object
        :return: The username of the user.
        """
        return "<User {}>".format(self.username)

class UserHasMessageSetting(db.Model):
    """User Message Seting Model"""

    __tablename__ = "user_message_settings"
    id = db.Column(db.BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True, index=True)
    suscriber_can_message = db.Column(db.Boolean,default=False)
    suscription_can_message = db.Column(db.Boolean,default=False)
    other_can_message = db.Column(db.Boolean,default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, user_id):
        """
        The function takes in a dictionary of keyword arguments and assigns the values to the class
        attributes
        """
        self.user_id = user_id

    def json(self):
    
        return {
            'user_id' : self.user_id,
            'suscriber_can_message': self.suscriber_can_message,
            'suscription_can_message': self.suscription_can_message,
            'other_can_message': self.other_can_message
        }

class UserHasCoin(db.Model):
    """User coins"""

    __tablename__ = "user_has_coins"
    id = db.Column(db.BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True, index=True)
    coins = db.Column(db.Integer,default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, user_id):
        """
        The function takes in a dictionary of keyword arguments and assigns the values to the class
        attributes
        """
        self.user_id = user_id
    
    def json(self): 
    
        return {
            'user_id': self.user_id,
            'coins':  self.coins
        }


