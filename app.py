
"""Blogly application."""
from flask import Flask, redirect, request, render_template, session, flash
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy.sql import text

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "oh-so-secret"

connect_db(app)        


@app.route('/')
def homepage():
    """Redirect to '/users' which will show a list of all users in db"""

    return redirect('/users')


@app.route('/users')
def show_users():
    """Show list of all users in db and can click on user's name to get user's information"""

    users = User.query.all()
    return render_template('show_users.html', users=users)
    
@app.route('/users/new')
def add_user_form():
    """Shows the add user form. Show a form to create a new user, object(instance)"""

    return render_template('add_user_form.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    """To create a new user, instance(object)"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show the details about that particular user"""

    user = User.query.get_or_404(user_id)      

    posts = Post.query.filter_by(user_id=user_id).all()      

    return render_template('user_details.html', user=user, posts=posts)


@app.route('/user/<user_id>/edit')
def edit_user_form(user_id):
    """Get the user's object(instance) and show the edit user form"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)


@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Update the user's information"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']


    db.session.add(user)
    db.session.commit()
   
    return redirect ('/users')

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>/posts/new')
def show_post_form(user_id):
    """Show the post form to the user"""

    user = User.query.get_or_404(user_id)

    tags = Tag.query.all()

    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Add a post to the user's detail page"""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    
    tags = request.form.getlist('tag_name')    
    for tag_name in tags:
        tag_object = Tag.query.filter(Tag.name==tag_name).first()  
        new_post.tags.append(tag_object)  
        db.session.add(new_post)        
        db.session.commit()

        return redirect(f'/users/{user_id}')


###############################################
#Post Routes
@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Show the details about a post"""

    post = Post.query.get(post_id)
   
    tags = post.tags

    return render_template('post_details.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show the form where the user can edit a post"""

    post = Post.query.get(post_id)
    
    tags = Tag.query.all()

    return render_template('edit_post_form.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Edit a post and save to db"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    
    tags = request.form.getlist('tag_name')   
        
    tag_objects = Tag.query.filter(Tag.name.in_(tags)).all()  
        
    post.tags = tag_objects  

    db.session.add(post)

    db.session.commit()
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a post"""

    post = Post.query.get(post_id)

    db.session.delete(post)

    db.session.commit()
    return redirect('/users')

#Tag Routes#########
@app.route('/tags')
def show_tags():
    """Show all tags"""

    tags = Tag.query.all()

    return render_template('show_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show tag details"""

    tag = Tag.query.get(tag_id)

    posts = tag.posts

    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def add_tag_form():
    """Show form to add a new tag"""

    return render_template('add_tag_form.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """Save the new tag information into db"""

    tag_name = request.form['tag_name']

    new_tag = Tag(name=tag_name)

    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Show form to edit a specific tag"""

    tag = Tag.query.get(tag_id)

    return render_template('edit_tag_form.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Save changed tag into db"""

    tag_name = request.form['tag_name']

    tag = Tag.query.get(tag_id)

    tag.name = tag_name

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tag/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag"""
    
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')

 