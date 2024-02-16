from mongoengine import Document, IntField, ObjectIdField, BooleanField, EnumField, FloatField, StringField, ListField, DictField

class Member(Document):
    
    # meta = {'collection': 'members'}
    # _id = ObjectIdField()
    userID = ObjectIdField()
    isPined = BooleanField(default=False)
    isMuted = BooleanField(default=False)
    isAdmin = BooleanField(default=False)
    isArchived = BooleanField(default=False)
    addedAt = FloatField()
    

class Discussion(Document):
    
    meta = {'collection': 'discussions'}
    _id = ObjectIdField()
    name = StringField()
    description = StringField()
    # tag = EnumField(enum=['PENDING', 'VALIDATED', 'DECLINED'])
    tag = StringField()
    createdBy = ObjectIdField()
    lastMessage = StringField(default=None)
    photoUrl  = StringField(default=None)
    updatedAt = FloatField(default=None)
    members = ListField(DictField())
    # members  = ListField(
    #     {
    #         'userID': ObjectIdField(),
    #         'isPined': BooleanField(default=False),
    #         'isMuted': BooleanField(default=False),
    #         'field': BooleanField(default=False),
    #         'isArchived': BooleanField(default=False),
    #         'addedAt': FloatField()
    #     }
    # )
    # status = EnumField(enum=['PENDING', 'VALIDATED', 'DECLINED'])