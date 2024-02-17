from mongoengine import Document, IntField, ObjectIdField, BooleanField, EnumField, FloatField, StringField, ListField, DictField

class Message(Document):
    
    meta = {'collection': 'messages'}
    _id = ObjectIdField()
    text = StringField()
    surveyId = ObjectIdField(default=None)
    senderId = ObjectIdField()
    discussionId = ObjectIdField()
    responseToMsgId = ObjectIdField(default=None)
    reactions = ListField(DictField())
    # file = DictField(default=None)
    type = StringField()
    createdAt = FloatField()
    

class Survey(Document):
    
    meta = {'collection': 'surveys'}
    _id = ObjectIdField()
    discussionId = ObjectIdField()
    question = StringField()
    creatorId = ObjectIdField()
    createdAt = FloatField()
    endedAt = FloatField()
    options = ListField(DictField())