from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField, TextAreaField

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