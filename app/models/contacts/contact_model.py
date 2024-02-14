from mongoengine import Document, IntField, ObjectIdField, BooleanField, EnumField, FloatField, StringField
from app.models.users.user_model import User

class ContactStatus:
    PENDING = "PENDING",
    VALIDATED = "VALIDATED"
    DECLINED = "DECLINED"

class Contact(Document):
    
    meta = {'collection': 'contacts'}
    _id = ObjectIdField()
    user1Id = ObjectIdField()
    user2Id = ObjectIdField()
    user1IdBlocked = BooleanField(default=False)
    user2IdBlocked = BooleanField(default=False)
    addedAt = FloatField()
    status = StringField(default='PENDING')
    # status = EnumField(enum=['PENDING', 'VALIDATED', 'DECLINED'])
    
    
    def to_json(self):
        
        user1 =  User.objects(_id = self.user1Id).first() 
        user2 =  User.objects(_id = self.user2Id).first()
                
        return {
            '_id': str(self._id),
            'user1' : user1.to_json() if user1 else None,
            'user2' : user2.to_json() if user2 else None,
            'user1IdBlocked' : self.user1IdBlocked,
            'user2IdBlocked' : self.user2IdBlocked,
            'addedAt' : self.addedAt,
            'status' :  self.status,
        }