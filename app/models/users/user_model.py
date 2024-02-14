"""User model."""
from mongoengine import connect, Document, StringField, ObjectIdField, EmbeddedDocument

class User(Document):
    
    meta = {'collection': 'users'}
    _id = ObjectIdField()
    email = StringField(max_length=200,unique=True,required=True)
    firstname = StringField(max_length=200,required=True)
    lastname = StringField(max_length=200, required=True)
    password = StringField(max_length=200, required=True)
    status = StringField()
    photoUrl = StringField()
    
    def to_json(self):
        
        return {
            '_id': str(self._id),
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'email' : self.email,
            'photoUrl' : self.photoUrl,
            'status' :  self.status,
        }