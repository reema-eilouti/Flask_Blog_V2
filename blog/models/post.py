from mongoengine import *
from .reply import Reply
from .user import User

import datetime


class Post(DynamicDocument):
    # define class metadata
    meta = {'collection': 'Posts',
            'indexes': [
                {'fields': ['$title', '$body'],
                 'default_language': 'english',
                 'weights': {'title': 10, 'body': 2}
                 }
            ]
            }

    # define class fields
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    body = StringField(required=True)
    likes = IntField(default=0)
    dislikes = IntField(default=0)
    comments = ListField(EmbeddedDocumentField(Reply))
