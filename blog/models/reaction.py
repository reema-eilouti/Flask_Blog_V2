from mongoengine import *
from .user import *
from .post import *


class Reaction(Document):

    meta = {'collection': 'reactions'}

    user = ReferenceField(User)
    post = ReferenceField(Post)
    like = BooleanField(default = False)
    dislike = BooleanField(default = False)