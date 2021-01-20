from mongoengine import *
from .reply import *
from .post import *


class User(DynamicDocument):
    # define class metadata
    meta = {'collection': 'users'}

    # define class fields
    username = StringField(required = True, primary_key = True)
    password = StringField(required = True)
    first_name = StringField(max_length = 50)
    last_name = StringField(max_length = 50)
    biography = StringField(max_length = 50)
    role = IntField(default = 0) 
    # favorite_posts = ListField(DynamicField(Post))



    def authenticate(self, username, password):
        # username / password -> from the login form
        # self.username / self.password -> from the database
        if username == self.username and password == self.password:
            return True
        else:
            return False



        # this method changes the user password
    
    

 # this method changes the user password
    def change_password(self, oldpassword, newpassword):
        if oldpassword == self.password:
            self.password = newpassword



