from mongoengine import *
from .user import *
import datetime


class Post(Document):
    # define class metadata
    meta = {'collection': 'Posts'}

    # define class fields
    author_id = ReferenceField(User)
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    body = StringField(required=True)
    likes = IntField(default=0)
    dislikes = IntField(default=0)



    