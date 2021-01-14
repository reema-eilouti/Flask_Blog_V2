from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField, TextAreaField

# Adding and Editing Posts Forms
class PostForm(FlaskForm):
    title = StringField("Post Title: ", [validators.InputRequired()] , render_kw = {"placeholder" : "Enter Post Title here"})
    body = TextAreaField("Post Body: ", [validators.InputRequired()], render_kw = {"placeholder" : "Enter Post Body here"})
    submit = SubmitField("Create Post")

class EditPostForm(FlaskForm):
    new_title = StringField("Post Title: ", [validators.InputRequired()])
    new_body = TextAreaField("Post Body: ", [validators.InputRequired()])
    submit = SubmitField("Edit")


# Adding and Editing Replies Forms
class ReplyPostForm(FlaskForm):
    body = TextAreaField("Reply Body: ", [validators.InputRequired()], render_kw = {"placeholder" : "Enter Your Reply here"})
    reply = SubmitField("Reply")

class EditReplyForm(FlaskForm):
    new_body = TextAreaField("Reply Body: ", [validators.InputRequired()])
    reply = SubmitField("Edit")


# Adding and Editing Users Forms
class AddUserForm(FlaskForm):
    username = StringField("Username : ", [validators.InputRequired()])
    password = PasswordField("Password : ", [validators.InputRequired()])
    first_name = StringField("First Name : ", [validators.InputRequired()])
    last_name = StringField("Last Name : ", [validators.InputRequired()])
    biography = TextAreaField("Biography : ")
    submit = SubmitField("Add User")

class EditUserInfoForm(FlaskForm):
    first_name = StringField("First Name : ", [validators.InputRequired()])
    last_name = StringField("Last Name : ", [validators.InputRequired()])
    biography = TextAreaField("Biography : ")
    edit = SubmitField("Edit User")


# Log In Account Settings Forms
class LoginForm(FlaskForm):
    username = StringField("Username : ", [validators.InputRequired()])
    password = PasswordField("Password : ", [validators.InputRequired()])
    submit = SubmitField("Log In")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password : ", [validators.InputRequired()])
    password = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm Password : ", [validators.InputRequired()])
    submit = SubmitField("Change Password")