from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField, TextAreaField

# Adding and Editing Replies Forms
class ReplyPostForm(FlaskForm):
    body = TextAreaField("Reply Body: ", [validators.InputRequired()], render_kw = {"placeholder" : "Enter Your Reply here"})
    reply = SubmitField("Reply")

class EditReplyForm(FlaskForm):
    new_body = TextAreaField("Reply Body: ", [validators.InputRequired()])
    reply = SubmitField("Edit")