from mongoengine import *
from .user import *
from .post import *
import datetime


class Reply(EmbeddedDocument):
    # define class metadata
    meta = {'collection': 'Replies'}

    # define class fields
    author = ReferenceField(User)
    created = DateTimeField(default=datetime.datetime.utcnow)
    body = StringField(required=True)
    


