from flask import Blueprint, render_template, request, redirect, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from blog.forms import LoginForm
from blog.models import User

# define our blueprint
login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST', 'GET'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        # read values from the login wtform
        username = login_form.username.data
        password = login_form.password.data

        user = User.objects(username=username).first()

        # if user  != None:
        # check if credentials are valid
        if user and user.password == password:
            # store the user ID in the session
            session['uid'] = str(user.id)
            session['username'] = user.username
            session['firstname'] = user.first_name
            session['lastname'] = user.last_name
            session['biography'] = user.biography
            session['role'] = user.role

        return redirect("/profile")

    # render the login template
    return render_template('login/login.html', form=login_form)


@login_bp.route('/logout')
def logout():
    # pop 'uid' from session
    session.clear()

    # redirect to index
    return redirect("/")
