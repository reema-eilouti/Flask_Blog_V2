from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import datetime
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from blog.forms import PostForm, ReplyPostForm, EditPostForm, EditReplyForm
from blog.models import Post , Reply , User , Reaction

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

            Post(author=session['username'], title=title, body=body).save()

            flash('Your post was successfully added')
            return redirect('/posts')

        #render the template
    return render_template("blog/index.html", form=add_post_form, posts=posts)



@post_bp.route('/latest-posts', methods=['GET', 'POST'])
@login_required
def latest_posts():

    posts = Post.objects().order_by('-created')
    
    return render_template("blog/latest-posts.html" , posts=posts)



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

        Post(author=session['username'], title=title, body=body).save()

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
    return render_template("blog/edit_post.html", form = edit_post_form)


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

@post_bp.route('/post/<post_id>/delete_reply/<reply_id>', methods=['GET', 'POST'])
@login_required
def delete_reply(post_id, reply_id):
    
    reply_id_int = int(reply_id)

    Post.objects(id = post_id).update_one(pull__comments__identification =  reply_id_int)

    # another solution for filtering
    # Post.objects(id = post_id).update_one(pull__comments__identification = Reply(identification = reply_id_int).identification)
    # $pull: {'content.assets': {'_id': ObjectId('4fc63def5b20fb722900010e')}
    

    

    return redirect(url_for('post.reply_post', post_id = post_id))
 

@post_bp.route('/post/<post_id>/edit_reply/<reply_id>', methods=['GET', 'POST'])
@login_required
def edit_reply(post_id, reply_id):

    edit_reply_form = EditReplyForm()

    post = Post.objects(id = post_id).first()

    reply_id_int = int(reply_id)

    reply_body = post.comments[reply_id_int -1].body



    if request.method == "GET":

        edit_reply_form.new_body.data = reply_body




    if edit_reply_form.validate_on_submit():
        
        reply_body = edit_reply_form.new_body.data

        post.comments[reply_id_int -1].body = reply_body

        post.save()

        return redirect(url_for("post.reply_post", post_id=post_id))




    return render_template("blog/edit_reply.html", form=edit_reply_form)


@post_bp.route("/post/<post_id>/like")
@login_required
def like(post_id):

    post = Post.objects(id = post_id).first()

    num_of_likes = post.likes

    num_of_dislikes = post.dislikes

    reaction_id = Reaction.objects(user = session['username'] , post = post_id).first()

    if reaction_id == None:
        
        post.likes = num_of_likes +1 

        reaction = Reaction(user = session['username'] , post = post_id , like = True , dislike = False).save()        
        
        post.save()
        

        return redirect(url_for("post.index"))

    elif reaction_id.favorite == True and reaction_id.like == None and reaction_id.dislike == None:
        

        num_of_likes += 1

        post.likes = num_of_likes

        post.save()

        reaction = Reaction.objects(id = reaction_id.id).first()
        reaction.like = True
        reaction.dislike = False
        reaction.save()

        return redirect(url_for("post.index"))


    elif reaction_id.like == True:

        reaction = Reaction.objects(id = reaction_id.id).first()
        reaction.like = True
        reaction.dislike = False
        
        post = Post.objects(id = post_id).first()
        post.likes = num_of_likes
        post.dislikes = num_of_dislikes
        
    

        return redirect(url_for("post.index"))

    elif reaction_id.dislike == True:

        reaction = Reaction.objects(id = reaction_id.id).first()
        reaction.like = True
        reaction.dislike = False
        reaction.save()
    
        post = Post.objects(id = post_id).first()
        post.likes = num_of_likes + 1
        post.dislikes = num_of_dislikes - 1
        post.save()

        return redirect(url_for("post.index"))


@post_bp.route("/post/<post_id>/dislike")
@login_required
def dislike(post_id):


    post = Post.objects(id = post_id).first()

    num_of_likes = post.likes

    num_of_dislikes = post.dislikes

    reaction_id = Reaction.objects(user = session['username'] , post = post_id).first()

    if reaction_id == None:

        post.dislikes = num_of_dislikes +1 

        reaction = Reaction(user = session['username'] , post = post_id , like = False , dislike = True).save()        
        
        post.save()

        return redirect(url_for("post.index"))

    elif reaction_id.favorite == True and reaction_id.like == False and reaction_id.dislike == False:

    
        num_of_dislikes += 1

        post.dislikes = num_of_dislikes

        post.save()

        reaction = Reaction.objects(id = reaction_id.id).first()
        reaction.like = False
        reaction.dislike = True
        reaction.save()


        return redirect(url_for("post.index"))

    elif reaction_id.dislike == True:

        reaction = Reaction.objects(id = reaction_id.id).first()
        reaction.like = False
        reaction.dislike = True
        

        post = Post.objects(id = post_id).first()
        post.likes = num_of_likes
        post.dislikes = num_of_dislikes
        

        return redirect(url_for("post.index"))

    elif reaction_id.like == True:

        reaction = Reaction.objects(id = reaction_id.id).first()
        reaction.like = False
        reaction.dislike = True
        reaction.save()
        

        post = Post.objects(id = post_id).first()
        post.likes = num_of_likes - 1
        post.dislikes = num_of_dislikes + 1
        post.save()



        return redirect(url_for("post.index"))


@post_bp.route("/post/<post_id>/favorite")
@login_required
def favorite(post_id):

    favorite_id = Reaction.objects(user = session['username'] , post = post_id).first()
   
    if favorite_id == None:

        favorite = Reaction(user = session['username'] , post = post_id , favorite = True).save()
        return redirect(url_for("post.index"))

    elif favorite_id.favorite == False :

        favorite = Reaction.objects(id = favorite_id.id).first()
        favorite.favorite = True
        
        favorite.save()

        return redirect(url_for("post.index"))

    elif favorite_id.favorite == True :
                    
        favorite = Reaction.objects(id = favorite_id.id).first()
        
        favorite.favorite = True
        
        favorite.save()

        return redirect(url_for("post.index"))

# unfinished text search
@post_bp.route("/posts/search", methods=['GET','POST'])
def search_posts():
    
    if request.method == 'POST':
        print("000000000000000000000000000000000000000000000000000000000000000000000000000000")
        search_keyword = str(request.form['search_keyword'])  
        posts = Post.objects.search_text(search_keyword).first()
        post_1 = posts.title
        print(post_1)
        print(posts)
        print("000000000000000000000000000000000000000000000000000000000000000000000000000000")

        return render_template("blog/search-posts.html" , posts = posts)


    

    
