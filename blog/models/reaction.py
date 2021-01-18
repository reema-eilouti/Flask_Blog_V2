from mongoengine import *
from .user import *
from .post import *

class Reaction(Document):
    user = ReferenceField(User)
    post = ReferenceField(Post)
    like = BooleanField(default = False)
    dislike = BooleanField(default = False)