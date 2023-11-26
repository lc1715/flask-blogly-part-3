
"""Blogly application."""
from flask import Flask, redirect, request, render_template, session, flash
from models import db, connect_db, User
from sqlalchemy.sql import text

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)        
# This is going to connect the Flask app (server) to SQLAlchemy. And then SQLAlchemy will 
# become the middle man between the Flask app and the database. 
# SQLAlchemy will turn the Python code in Flask to SQL code for the database.
# We are going to put the Flask app, named app, into the function, connect_db, 
# and run that function so that SQLAlchemy will now be connected to the Flask app.
# db.create_all()

@app.route('/')
def homepage():
    """Redirect to '/users' which will show a list of all users in db"""

    return redirect('/users')


@app.route('/users')
def show_users():
    """Show list of all users in db and can click on user's name to get user's information"""

    users = User.query.all()
    return render_template('show_users.html', users=users)
    #users returns a list with objects in it. the users are the objects.
    # users = [<User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png,
    # <User id=2 first_name=Joel last_name=Burton image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png]

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
    #Have to write this line so that if the user does not put in an image url,
    #then the value for the image url will be None. If the image_url 
    # has a value of None, then the image-url will take the default image_url.
    # Apparently you can also write image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    #So if the image_url has a value of None, then the image-url will take the default url

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')
#To create a new user, instance(object), and save it to the db.
# We are getting the info from the form in which the user typed in his information (first name, last name and url).
# We are creating a new user, instance(object) with the info from the form.
#We are adding that new user, instance(object) to the database.


@app.route('/users/<user_id>')
def user_details(user_id):
    """Show the details about that particular user"""

    user = User.query.get_or_404(user_id)      #getting the user's info out of the database
    return render_template('user_details.html', user=user)


@app.route('/user/<user_id>/edit')
def edit_user_form(user_id):
    """Get the user's object(instance) and show the edit user form"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)


@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Update the user's information"""

    user = User.query.get_or_404(user_id)
    #Get the user, object(instance) of the user they're trying to edit

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    #Getting the user's inputs from the form and update 
    # the user's first name, last name, and url with 
    # whatever the user typed into form

    db.session.add(user)
    db.session.commit()
    #Adding the updated user's first name, last name, and url to the database
    return redirect ('/users')
# <!-- We are getting the user's info out of this user object but writing the name fo the object and then the key-name.-->
# <!-- user = {User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png} -->

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""

    User.query.filter_by(id = user_id).delete()     
    db.session.commit()
    return redirect('/users')
#Have to use just instance attribute, id, and then the value when using filter_by

 #users returns a list with objects in it. the users are the objects.
#users = 
# [<User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png,
#  <User id=2 first_name=Joel last_name=Burton image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png]
#user = {User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png}






# My Original Solution which completely works great!=
# """Blogly application."""

# from flask import Flask, redirect, request, render_template, session, flash
# from models import db, connect_db, User
# from sqlalchemy.sql import text


# app = Flask(__name__)
# app.app_context().push()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
# app.config['SQLALCHEMY_ECHO'] = True

# connect_db(app)        
# # This is going to connect the Flask app (server) to SQLAlchemy. And then SQLAlchemy will 
# # become the middle man between the Flask app and the database. 
# # SQLAlchemy will turn the Python code in Flask to SQL code for the database.
# # We are going to put the Flask app, named app, into the function, connect_db, 
# # and run that function so that SQLAlchemy will now be connected to the Flask app.

# # db.create_all()


# @app.route('/')
# def homepage():
#     """Redirect to '/users' which will show a list of all users in db"""
#     return redirect('/users')

# @app.route('/users')
# def show_users():
#     """Show list of all users in db and can click on user's name to get user's information"""

#     users = User.query.all()
#     return render_template('show_users.html', users=users)
#     #users returns a list with objects in it. the users are the objects.
#     # users = [<User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png,
#     # <User id=2 first_name=Joel last_name=Burton image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png]


# @app.route('/users/new')
# def add_user_form():
#     """Shows the add user form. Show a form to create a new user, object(instance)"""

#     return render_template('add_user_form.html')


# @app.route('/users/new', methods=["POST"])
# def add_user():
#     """To create a new user, instance(object)"""

#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     image_url = request.form['image_url']
#     image_url = image_url if image_url else None
#     #Have to write this line so that if the user does not put in an image url,
#     #then the value for the image url will be None. If the image_url 
#     # has a value of None, then the image-url will take the default image_url.

#     new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
#     #So if the image_url has a value of None, then the image-url will take the default url

#     db.session.add(new_user)
#     db.session.commit()

#     return redirect('/users')
# #To create a new user, instance(object), and save it to the db.
# # We are getting the info from the form in which the user typed in his information (first name, last name and url).
# # We are creating a new user, instance(object) with the info from the form.
# #We are adding that new user, instance(object) to the database.

# @app.route('/users/<user_id>')
# def user_details(user_id):
#     """Show the details about that particular user"""

#     user = User.query.get(user_id)      #getting the user's info out of the database

#     return render_template('user_details.html', user=user)


# @app.route('/user/<user_id>/edit')
# def edit_user_form(user_id):
#     """Get the user's object(instance) and show the edit user form"""

#     user = User.query.get(user_id)

#     return render_template('edit_user_form.html', user=user)


# @app.route('/users/<user_id>/edit', methods=["POST"])
# def edit_user(user_id):
#     """Update the user's information"""

#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     image_url = request.form['image_url']
#     #Getting the user's inputs from the form

#     user = User.query.get(user_id)
#     #Get the user, object(instance) of the user they're trying to edit

#     user.first_name = first_name
#     user.last_name = last_name
#     user.image_url =  image_url
#     #Actually update the user's first name, last name, and url with whatever the user typed into form

#     db.session.add(user)
#     db.session.commit()
#     #Adding the updated user's first name, last name, and url to the database

#     return redirect ('/users')
# # <!-- We are getting the user's info out of this user object but writing the name fo the object and then the key-name.-->
# # <!-- user = {User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png} -->


# @app.route('/users/<user_id>/delete')
# def delete_user(user_id):
#     """Delete a user"""

#     User.query.filter_by(id = user_id).delete()     

#     db.session.commit()

#     return redirect('/users')
# #Have to use just instance attribute, id, and then the value when using filter_by


#  #users returns a list with objects in it. the users are the objects.
# #users = 
# # [<User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png,
# #  <User id=2 first_name=Joel last_name=Burton image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png]

# #user = {User id=1 first_name=Alan last_name=Alda image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png}



# How to add a user into the database=
# lc131715@Lisa:~/backend exercises springboard/sqlalchemy exercises/flask-blogly$ ls
# __pycache__  app.py  models.py  requirements.txt  seed.py  templates  test_flask.py  venv
# lc131715@Lisa:~/backend exercises springboard/sqlalchemy exercises/flask-blogly$ ipython
# Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0]
# Type 'copyright', 'credits' or 'license' for more information
# IPython 8.14.0 -- An enhanced Interactive Python. Type '?' for help.

# In [1]: %run app.py
# 'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.

# In [2]: lori = User(first_name='Lori', last_name='Litow')

# In [3]: lori
# Out[3]: <User id=None first_name=Lori last_name=Litow image_url=None

# In [4]: db.session.add(lori)

# In [5]: db.session.commit()
# 2023-11-20 23:27:43,085 INFO sqlalchemy.engine.Engine select pg_catalog.version()
# 2023-11-20 23:27:43,085 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-20 23:27:43,087 INFO sqlalchemy.engine.Engine select current_schema()
# 2023-11-20 23:27:43,087 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-20 23:27:43,088 INFO sqlalchemy.engine.Engine show standard_conforming_strings
# 2023-11-20 23:27:43,088 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-20 23:27:43,089 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 23:27:43,091 INFO sqlalchemy.engine.Engine INSERT INTO users (first_name, last_name, image_url) VALUES (%(first_name)s, %(last_name)s, %(image_url)s) RETURNING users.id
# 2023-11-20 23:27:43,091 INFO sqlalchemy.engine.Engine [generated in 0.00026s] {'first_name': 'Lori', 'last_name': 'Litow', 'image_url': 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'}
# 2023-11-20 23:27:43,093 INFO sqlalchemy.engine.Engine COMMIT

# In [6]: lori
# Out[6]: 2023-11-20 23:27:54,012 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 23:27:54,014 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 23:27:54,014 INFO sqlalchemy.engine.Engine [generated in 0.00029s] {'pk_1': 7}
# <User id=7 first_name=Lori last_name=Litow image_url=https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png


# # Springboard Solution =
# from flask import Flask, request, redirect, render_template
# from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db, User

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'ihaveasecret'

# # Having the Debug Toolbar show redirects explicitly is often useful;
# # however, if you want to turn it off, you can uncomment this line:
# #
# # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)


# connect_db(app)
# db.create_all()


# @app.route('/')
# def root():
#     """Homepage redirects to list of users."""

#     return redirect("/users")


# ##############################################################################
# # User route

# @app.route('/users')
# def users_index():
#     """Show a page with info on all users"""

#     users = User.query.order_by(User.last_name, User.first_name).all()
#     return render_template('users/index.html', users=users)


# @app.route('/users/new', methods=["GET"])
# def users_new_form():
#     """Show a form to create a new user"""

#     return render_template('users/new.html')


# @app.route("/users/new", methods=["POST"])
# def users_new():
#     """Handle form submission for creating a new user"""

#     new_user = User(
#         first_name=request.form['first_name'],
#         last_name=request.form['last_name'],
#         image_url=request.form['image_url'] or None)

#     db.session.add(new_user)
#     db.session.commit()

#     return redirect("/users")


# @app.route('/users/<int:user_id>')
# def users_show(user_id):
#     """Show a page with info on a specific user"""

#     user = User.query.get_or_404(user_id)
#     return render_template('users/show.html', user=user)


# @app.route('/users/<int:user_id>/edit')
# def users_edit(user_id):
#     """Show a form to edit an existing user"""

#     user = User.query.get_or_404(user_id)
#     return render_template('users/edit.html', user=user)


# @app.route('/users/<int:user_id>/edit', methods=["POST"])
# def users_update(user_id):
#     """Handle form submission for updating an existing user"""

#     user = User.query.get_or_404(user_id)
#     user.first_name = request.form['first_name']
#     user.last_name = request.form['last_name']
#     user.image_url = request.form['image_url']

#     db.session.add(user)
#     db.session.commit()

#     return redirect("/users")


# @app.route('/users/<int:user_id>/delete', methods=["POST"])
# def users_destroy(user_id):
#     """Handle form submission for deleting an existing user"""

#     user = User.query.get_or_404(user_id)
#     db.session.delete(user)
#     db.session.commit()

#     return redirect("/users")