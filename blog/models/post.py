from mongoengine import *
from .reply import Reply 
from .user import User

import datetime


class Post(Document):
    # define class metadata
    meta = {'collection': 'Posts'}

    # define class fields
    author = ReferenceField(User, reverse_delete_rule = CASCADE)
    created = DateTimeField(default = datetime.datetime.utcnow)
    title = StringField(required = True)
    body = StringField(required = True)
    likes = IntField(default = 0)
    dislikes = IntField(default = 0)
    comments = ListField(EmbeddedDocumentField(Reply))



    