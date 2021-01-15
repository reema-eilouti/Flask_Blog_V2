from flask import Blueprint, render_template,request ,redirect, session , flash,url_for
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField 
from blog.forms import AddUserForm, EditUserInfoForm, ChangePasswordForm
from blog.models import User, Post

# define our blueprint
user_bp = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)

    
    def check(*args, **kwargs):
        

        if 'username' in session:
            return f(*args, **kwargs)
            
        else:

            return redirect('/login')
            
            
    return check



@user_bp.route('/change_password' , methods=['POST' , 'GET'])
@login_required
def change_password():

    change_form = ChangePasswordForm()
    
    if change_form.validate_on_submit():
        oldpassword = change_form.old_password.data
        newpassword = change_form.password.data
    
        
        user = User.objects(username = session['username']).first()

        if oldpassword ==  user.password :
            if oldpassword != newpassword :

                user.password = newpassword
                user.save()
            
            else :
                flash("New password can not be same the old password")
                return redirect(url_for("user.change_password"))

        else:
            flash("Incorrect Password")
            return redirect(url_for("user.change_password"))

        return redirect(url_for("user.profile"))    


    return render_template('user/change_password.html' , form = change_form )



@user_bp.route('/session')
def show_session():
    return dict(session)



@user_bp.route('/add/user', methods=['GET', 'POST'])
#@login_required
def add_user():

    add_user_form = AddUserForm()

    if add_user_form.validate_on_submit():

        user = User()
    
        user.username = add_user_form.username.data
        user.password = add_user_form.password.data
        user.first_name = add_user_form.first_name.data
        user.last_name = add_user_form.last_name.data
        user.biography = add_user_form.biography.data

        user.save()        

        return redirect("/users")

    return render_template('user/index.html' , form = add_user_form )



@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    user = User.objects(username = session['uid'])

    posts = Post.objects(author_id = session['uid']).order_by('-created')

        
    flash('You were successfully logged in')

    return render_template("user/profile.html", user = user, posts = posts ) 



@user_bp.route('/edit/user', methods=['GET', 'POST'])
@login_required
def edit_user():

    edit_form = EditUserInfoForm() 
    
    if request.method == "GET":

    #set values in the form
        edit_form.first_name.data = session['firstname']
        edit_form.last_name.data = session['lastname']
        edit_form.biography.data = session['biography']

    if  edit_form.validate_on_submit():

        new_firstname = edit_form.first_name.data
        new_lastname = edit_form.last_name.data
        new_bio = edit_form.biography.data

        user = User.objects(username = session["username"]).first()

        user.first_name = new_firstname
        user.last_name = new_lastname
        user.biography = new_bio 

        user.save()

        session['firstname'] = new_firstname
        session['lastname'] = new_lastname
        session['biography'] = new_bio

        return redirect('/profile') 

    return render_template("user/edituser.html", form = edit_form)



@user_bp.route('/users')
@login_required
def get_users():
    # get the DB connection
    db = get_db()

    # get all users from the db
    users = db.execute('select * from user').fetchall()

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)



@user_bp.route('/users/<int:user_id>')
@login_required
def delete_user(user_id):
    # get the DB connection
    db = get_db()

    db.execute(f"DELETE FROM user WHERE id = {user_id} ")
    db.commit()

    return redirect(url_for("user.get_users"))