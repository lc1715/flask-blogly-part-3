"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_image_url = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'


class User(db.Model):
    """class(model) that has user instance attributes and methods. It is equal to the sql table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String, nullable=False)
    
    last_name = db.Column(db.String, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=default_image_url)
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}"
    




# # My Original Solution = 
# class User(db.Model):
#     """class(model) that has user instance attributes and methods. It is equal to the sql table"""
    
#     __tablename__ = 'users'

#     id = db.Column(db.Integer,
#                    primary_key=True,
#                    autoincrement=True)
    
#     first_name = db.Column(db.String, nullable=False)
    
#     last_name = db.Column(db.String, nullable=False)

#     image_url = db.Column(db.String, nullable=False, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')
    
#     def __repr__(self):
#         u = self
#         return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}"





# default_image_url = 'https://images.unsplash.com/photo-1568572933382-74d440642117?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8ZG9nc3xlbnwwfHwwfHx8MA%3D%3D'

# default_image_url = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'
    
