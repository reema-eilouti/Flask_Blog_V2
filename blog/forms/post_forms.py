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