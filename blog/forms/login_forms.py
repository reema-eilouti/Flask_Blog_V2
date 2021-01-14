from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField, TextAreaField

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