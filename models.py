"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_image_url = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'


class User(db.Model):
    """class(model) that has user instance attributes and methods. It is equal to the sql table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    first_name = db.Column(db.String, nullable=False)
    
    last_name = db.Column(db.String, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=default_image_url)
 
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")  
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url} posts={u.posts}>"
    

class Post(db.Model):
    """Post model(class)"""
    
    __tablename__ = 'posts'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')
   
    @property
    def friendly_date(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        p = self  
        return f"Post id={p.id} title={p.title} content={p.content} created_at={p.friendly_date} user_id={p.user_id} user={p.user}"




class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String, nullable=False, unique=True )

    def __repr__(self):
        t = self
        return f'Tag id={t.id} name={t.name}'


class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        pt = self
        return f'PostTag post_id={pt.post_id} tag_id={pt.tag_id}'

