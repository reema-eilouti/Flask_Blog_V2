from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import datetime
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from blog.forms import PostForm, ReplyPostForm, EditPostForm, EditReplyForm
from blog.models import Post , Reply , User

# define our blueprint
post_bp = Blueprint('post', __name__)


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):

        if 'username' in session:
            return f(*args, **kwargs)

        else:
            return redirect('/login')
    return check


@post_bp.route('/', methods=['GET', 'POST'])
@post_bp.route('/posts', methods=['GET', 'POST'])
@login_required
def index():

    add_post_form = PostForm()

    if request.method == "GET":

        posts = Post.objects

    else:

        if add_post_form.validate_on_submit():

            # read post values from the form
            title = add_post_form.title.data
            body = add_post_form.body.data

            post = Post.objects(username=session['username'])
            post.title = title
            post.body = body

            flash('Your post was successfully added')
            return redirect('/posts')

        # if the user is not logged in, redirect to '/login'
        if "username" not in session:
            return redirect('/login')

        # else, render the template
    return render_template("blog/index.html", form=add_post_form, posts=posts)


@post_bp.route('/myposts')
@login_required
def myposts():

    posts = Post.objects(author=session['username'])

    # render 'blog' blueprint with posts
    return render_template('blog/myposts.html', posts=posts)


@post_bp.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():

    post_form = PostForm()

    if post_form.validate_on_submit():
        # read post values from the form
        title = post_form.title.data
        body = post_form.body.data

        post = Post(author=session['username'], title=title, body=body).save()

        flash('You were successfully Add')
        return redirect('/posts')

    # else, render the template
    return render_template("blog/add-post.html", form=post_form)


@post_bp.route('/post/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    Post.objects(id=post_id).first().delete()

    return redirect(url_for("post.myposts"))


@post_bp.route('/post/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    post = Post.objects(id=post_id).first()
    edit_post_form = EditPostForm()

    if request.method == "GET":

        edit_post_form.new_title.data = post.title
        edit_post_form.new_body.data = post.body

    if edit_post_form.validate_on_submit():
        # read post values from the form
        post.title = edit_post_form.new_title.data  # title
        post.body = edit_post_form.new_body.data  # content

        post.save()

        return redirect(url_for("post.myposts"))

    # else, render the template
    return render_template("blog/edit_post.html", form=edit_post_form)


@post_bp.route('/post/<post_id>/add_reply', methods=['GET', 'POST'])
@login_required
def reply_post(post_id):
    
    reply_form = ReplyPostForm()

    if reply_form.validate_on_submit():
       
        post = Post.objects(id = post_id).first()
        
        user = User.objects(username = session['username']).first()

        identifications = []

        for i in range(len(post.comments)):

            identifications.append(post.comments[i].identification)

        maximum_id = max(identifications)

        reply = Reply(identification = maximum_id + 1  ,body = reply_form.body.data , author = user)
        
        post.comments.append(reply)

        post.save()

        return redirect(url_for('post.reply_post', post_id=post_id))

  
    # Display the reply section

    # retrieve post
    post = Post.objects(id = post_id).first()
    

   
    # render the template
    return render_template("blog/reply_post.html", mypost = post, form = reply_form)

# unfinished function ***** 
@post_bp.route('/post/<post_id>/delete_reply/<reply_id>', methods=['GET', 'POST'])
@login_required
def delete_reply(post_id, reply_id):
    
    integer = int(reply_id)
    post = Post.objects(id = post_id).first()
    
    # post.comments[integer](identification = reply_id).first().delete()

    Reply.objects(identification = reply_id).delete()
    
    return redirect(url_for('post.reply_post', post_id=post_id))
 

@post_bp.route('/post/<post_id>/edit_reply', methods=['GET', 'POST'])
@login_required
def edit_reply(post_id, reply_id):

    edit_reply_form = EditReplyForm()

    if request.method == "GET":

        db = get_db()

        current_reply = db.execute(
            f"select * from reply WHERE id = {reply_id}").fetchone()

        edit_reply_form.new_body.data = current_reply['body']

    if edit_reply_form.validate_on_submit():
        # read post values from the form
        new_body = edit_reply_form.new_body.data

        # get the DB connection
        db = get_db()

        try:

            db.execute(
                f"UPDATE reply SET body = '{new_body}' WHERE id = '{reply_id}' ")

            # commit changes to the database
            db.commit()

            return redirect(url_for("blog.reply_post", post_id=post_id))

        except sqlite3.Error as er:
            print(f"SQLite error: { (' '.join(er.args)) }")
            return redirect("/404")

    # if the user is not logged in, redirect to '/login'
    if "uid" not in session:
        return redirect('/login')

    # else, render the template
    return render_template("blog/edit_reply.html", form=edit_reply_form)


@post_bp.route("/post/<post_id>/like")
@login_required
def like(post_id):

    db = get_db()

    num_of_likes = db.execute(
        "SELECT likes FROM post WHERE id LIKE ?", (post_id,)).fetchone()
    total_likes = num_of_likes['likes']

    num_of_dislikes = db.execute(
        "SELECT dislikes FROM post WHERE id LIKE ?", (post_id,)).fetchone()
    total_dislikes = num_of_dislikes['dislikes']

    reaction_id = db.execute(
        f"SELECT * FROM reaction WHERE user_id = {session['uid']} AND post_id = {post_id}").fetchone()

    if reaction_id == None:

        db = get_db()

        total_likes += 1

        db.execute(
            f"UPDATE post SET likes = {total_likes} WHERE id = {post_id}")

        db.execute(f"INSERT INTO reaction (post_id, user_id, like, dislike) VALUES (?, ?, ?, ?);",
                   (post_id, session['uid'], 1, 0))

        db.commit()

        return redirect(url_for("blog.index"))

    elif reaction_id['favorite'] == 1 and reaction_id['like'] == None and reaction_id['dislike'] == None:

        db = get_db()

        total_likes += 1

        db.execute(
            f"UPDATE post SET likes = {total_likes} WHERE id = {post_id}")

        db.execute(f"update reaction set like = {1} , dislike = {0}")

        db.commit()

        return redirect(url_for("blog.index"))

    elif reaction_id['like'] == 1:

        db.execute(
            f"UPDATE reaction SET like = '{1}', dislike = '{0}' WHERE id = '{reaction_id['id']}'")

        db.execute(
            f"UPDATE post SET likes = '{total_likes}', dislikes = '{total_dislikes}' WHERE id = {post_id}")

        db.commit()

        return redirect(url_for("blog.index"))

    elif reaction_id['dislike'] == 1:

        db.execute(
            f"UPDATE reaction SET like = '{1}', dislike = '{0}' WHERE id = '{reaction_id['id']}'")

        db.execute(
            f"UPDATE post SET likes = '{total_likes + 1}', dislikes = '{total_dislikes - 1}' WHERE id = {post_id}")

        db.commit()

        return redirect(url_for("blog.index"))


@post_bp.route("/post/<post_id>/dislike")
@login_required
def dislike(post_id):

    db = get_db()

    num_of_likes = db.execute(
        "SELECT likes FROM post WHERE id LIKE ?", (post_id,)).fetchone()
    total_likes = num_of_likes['likes']

    num_of_dislikes = db.execute(
        "SELECT dislikes FROM post WHERE id LIKE ?", (post_id,)).fetchone()

    total_dislikes = num_of_dislikes['dislikes']

    reaction_id = db.execute(
        f"SELECT * FROM reaction WHERE user_id = {session['uid']} AND post_id = {post_id}").fetchone()

    if reaction_id == None:

        db = get_db()

        total_dislikes += 1

        db.execute(
            f"UPDATE post SET dislikes = {total_dislikes} WHERE id = {post_id}")

        db.execute(f"INSERT INTO reaction (post_id, user_id, like, dislike) VALUES (?, ?, ?, ?);",
                   (post_id, session['uid'], 0, 1))

        db.commit()

        return redirect(url_for("blog.index"))

    elif reaction_id['favorite'] == 1 and reaction_id['like'] == None and reaction_id['dislike'] == None:

        db = get_db()

        total_dislikes += 1

        db.execute(
            f"UPDATE post SET dislikes = {total_dislikes} WHERE id = {post_id}")

        db.execute(f"UPDATE reaction  SET like = {0} , dislike = {1}")

        db.commit()

        return redirect(url_for("blog.index"))

    elif reaction_id['dislike'] == 1:

        db.execute(
            f"UPDATE reaction SET like = '{0}', dislike = '{1}' WHERE id = '{reaction_id['id']}'")

        db.execute(
            f"UPDATE post SET likes = '{total_likes}', dislikes = '{total_dislikes}' WHERE id = {post_id}")

        db.commit()

        return redirect(url_for("blog.index"))

    elif reaction_id['like'] == 1:

        db.execute(
            f"UPDATE reaction SET like = '{0}', dislike = '{1}' WHERE id = '{reaction_id['id']}'")

        db.execute(
            f"UPDATE post SET likes = '{total_likes - 1}', dislikes = '{total_dislikes + 1}' WHERE id = {post_id}")

        db.commit()

        return redirect(url_for("blog.index"))


@post_bp.route("/post/<post_id>/favorite")
@login_required
def favorite(post_id):

    db = get_db()

    favorite_id = db.execute(
        f"select * from reaction where post_id = {post_id} and user_id = {session['uid']}").fetchone()

    if favorite_id == None:

        db.execute(f"INSERT INTO reaction (post_id , user_id , favorite) VALUES (?,?,?);",
                   (post_id, session['uid'], 1))

        db.commit()

        return redirect(url_for("blog.index"))

    elif favorite_id['favorite'] == None:

        db.execute(
            f"UPDATE reaction SET favorite = '{1}' WHERE id = {favorite_id['id']}")

        db.commit()

        return redirect(url_for("blog.index"))
