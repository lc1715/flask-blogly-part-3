"""Seed file to make sample data for blogly db"""

from models import User, db, Post, Tag, PostTag      
from app import app          

#Create all tables
db.drop_all()         
db.create_all()         

#If table isn't empty, empty it
User.query.delete()     
Tag.query.delete()
PostTag.query.delete()


#Add users
lori = User(first_name='Lori', last_name='Lam')           
paul = User(first_name='Paul', last_name='Rivers')


#Add tags:
tag1 = Tag(name='Greetings')
tag2 = Tag(name='Animals')


# Add new objects to session, so they'll persist
db.session.add_all([lori, paul, tag1, tag2]) 
db.session.commit()


#Add posts:
p1 = Post(title='Hello Post', content='Enjoy each day!', user_id=1, user=lori)
p2 = Post(title='Dogs Post', content='Dogs are the best!', user_id=2, user=paul)


# Add new objects to session, so they'll persist
db.session.add_all([p1, p2]) 
db.session.commit()


