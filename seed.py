"""Seed file to make sample data for blogly db"""

from models import User, db      #import the model(class), Pet, and db (db = SQLALchemy) from the models.py file
from app import app             #import app from the app.py file

#Create all tables
db.drop_all()           #drops all of the tables in our db
db.create_all()         #creates all of the tables from the models, classes

#If table isn't empty, empty it
User.query.delete()      #to empty out the entire pets table. To delete ALL of the pets inside of the pets table at once.

#Add pets
lori = User(first_name='Lori', last_name='Litow')            #create new pet instances (objects)
paul = User(first_name='Paul', last_name='Pill')
# spike = Pet(name='Spike', species='porcupine')

# Add new objects to session, so they'll persist
db.session.add(lori)                    #Add the pets, instances (objects), rows to the session
db.session.add(paul)
# db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()                 #Add the pets, instances (objects), rows to the database

#If you do run this file, you'll delete everything out of your pets table and database
#that you currently have now and recreate them with this data inside of it. 
# I think you just do %run seed.py in ipython to run this file. 
#In this file we're not dropping (deleting) the database, we're just dropping 
#all of the tables and everything inside of the tables that's in this database.
# Everything that SQAlchemy knows about which are the tables and everything
# inside of the tables will be dropped and then we add new data in.