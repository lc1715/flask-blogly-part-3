from unittest import TestCase   
from app import app             # Importing Flask (app) from the ap.py file
from models import db, User     #Importing SQLAlchemy (db) and the class User from models.py file


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'   #creates a new test database called sqla_intro_test database   
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()               #deleting all tables in the sqla_intro_test db
db.create_all()             #creating new table in the sqla_intro_test db which is really just the users table which is equal to the class (model) User


class UserTestCase(TestCase):

    def setUp(self):            # this will run before every single testing method below
        """Add sample user."""

        User.query.delete()      # delete all existing users in the pets table

        user = User(first_name='Paul', last_name='Pill', image_url='http://sample')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        #Remember, self is going to equal to the object (instance), user. Since user is
        #equal to an object, I can access all of the key-value pairs in that object.

    def tearDown(self):      # this will run after each testing method has run
        """Clean up the session (db.session) in case there's any messed up savings in session (db.session)"""
        db.session.rollback()       #clears up the session (db.session) after test method has run so it'll be clean for next test method


    def test_show_users(self):
        """Test the route '/users/' will show all users"""

        with app.test_client() as client:       #Remember, client is equal to the fake server 
            resp= client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Paul', html)


    def test_add_user(self):
        """"Test that a get request to the '/users/new' route will show te add user form """
        with app.test_client() as client:
            data = {'first_name':'Lori', 'last_name':'Litow', 'image_url':'http://fakeprofilepic'}
            res = client.post('/users/new', data=data, follow_redirects=True)   #I didn't write the first test function to test that we get a status code of 302. I just went straight to the redirected route to get hte status code of 200 and the html response
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Lori', html)
    # I didn't write the first redirect test function to test that we get a status code 
    # of 302. I just went straight to the redirected route to get the status code of 200 
    # and the html response. It's best to test both in future. Very simple my notes will 
    #show how to do both. I did write the first redirect test function for 
    # test_edit_user_302 below.

    def test_edit_user_form(self):
        """Test that get request to '/user/{self.user_id}/edit' will get the user's object 
        and show the edit user form """

        with app.test_client() as client:
            res = client.get(f'/user/{self.user_id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Paul', html)


    def test_edit_user_302(self):
        """Test that the first request in redirect Post request to '/users/{self.user_id}/edit' 
        will lead to 302 status code and redirect to '/users' """

        with app.test_client() as client:
            data = {'first_name':'David', 'last_name':'Schwartz', 'image_url':'http://fakeprofilepic'}
            res = client.post(f'/users/{self.user_id}/edit', data=data)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')


    def test_edit_user(self):
        """Test that 2nd request in redirect Post request to '/users/{self.user_id}/edit'
        will update the user's info and redirect to show all of the users"""
        
        with app.test_client() as client:
            data = {'first_name':'David', 'last_name':'Schwartz', 'image_url':'http://fakeprofilepic'}
            res = client.post(f'/users/{self.user_id}/edit', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('David', html)



#Write, python3 -m unittest test_flask.py, to run tests in regular Terminal=
# lc131715@Lisa:~/backend exercises springboard/sqlalchemy exercises/flask-blogly$ python3 -m unittest test_flask.py
# 'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
# 2023-11-20 21:13:40,207 INFO sqlalchemy.engine.Engine select pg_catalog.version()
# 2023-11-20 21:13:40,207 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-20 21:13:40,208 INFO sqlalchemy.engine.Engine select current_schema()
# 2023-11-20 21:13:40,208 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-20 21:13:40,208 INFO sqlalchemy.engine.Engine show standard_conforming_strings
# 2023-11-20 21:13:40,208 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-20 21:13:40,209 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,212 INFO sqlalchemy.engine.Engine SELECT pg_catalog.pg_class.relname
# FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
# WHERE pg_catalog.pg_class.relname = %(table_name)s AND pg_catalog.pg_class.relkind = ANY (ARRAY[%(param_1)s, %(param_2)s, %(param_3)s, %(param_4)s, %(param_5)s]) AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != %(nspname_1)s
# 2023-11-20 21:13:40,212 INFO sqlalchemy.engine.Engine [generated in 0.00024s] {'table_name': 'users', 'param_1': 'r', 'param_2': 'p', 'param_3': 'f', 'param_4': 'v', 'param_5': 'm', 'nspname_1': 'pg_catalog'}
# 2023-11-20 21:13:40,214 INFO sqlalchemy.engine.Engine
# DROP TABLE users
# 2023-11-20 21:13:40,214 INFO sqlalchemy.engine.Engine [no key 0.00021s] {}
# 2023-11-20 21:13:40,216 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,224 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,225 INFO sqlalchemy.engine.Engine SELECT pg_catalog.pg_class.relname
# FROM pg_catalog.pg_class JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_catalog.pg_class.relnamespace
# WHERE pg_catalog.pg_class.relname = %(table_name)s AND pg_catalog.pg_class.relkind = ANY (ARRAY[%(param_1)s, %(param_2)s, %(param_3)s, %(param_4)s, %(param_5)s]) AND pg_catalog.pg_table_is_visible(pg_catalog.pg_class.oid) AND pg_catalog.pg_namespace.nspname != %(nspname_1)s
# 2023-11-20 21:13:40,225 INFO sqlalchemy.engine.Engine [cached since 0.01317s ago] {'table_name': 'users', 'param_1': 'r', 'param_2': 'p', 'param_3': 'f', 'param_4': 'v', 'param_5': 'm', 'nspname_1': 'pg_catalog'}
# 2023-11-20 21:13:40,226 INFO sqlalchemy.engine.Engine
# CREATE TABLE users (
#         id SERIAL NOT NULL,
#         first_name VARCHAR NOT NULL,
#         last_name VARCHAR NOT NULL,
#         image_url VARCHAR NOT NULL,
#         PRIMARY KEY (id)
# )


# 2023-11-20 21:13:40,226 INFO sqlalchemy.engine.Engine [no key 0.00019s] {}
# 2023-11-20 21:13:40,238 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,243 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,243 INFO sqlalchemy.engine.Engine DELETE FROM users
# 2023-11-20 21:13:40,243 INFO sqlalchemy.engine.Engine [generated in 0.00013s] {}
# 2023-11-20 21:13:40,246 INFO sqlalchemy.engine.Engine INSERT INTO users (first_name, last_name, image_url) VALUES (%(first_name)s, %(last_name)s, %(image_url)s) RETURNING users.id
# 2023-11-20 21:13:40,246 INFO sqlalchemy.engine.Engine [generated in 0.00020s] {'first_name': 'Paul', 'last_name': 'Pill', 'image_url': 'http://sample'}
# 2023-11-20 21:13:40,247 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,250 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,251 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,251 INFO sqlalchemy.engine.Engine [generated in 0.00019s] {'pk_1': 1}
# /home/lc131715/.local/lib/python3.10/site-packages/flask/testing.py:116: DeprecationWarning: The '__version__' attribute is deprecated and will be removed in Werkzeug 3.1. Use feature detection or 'importlib.metadata.version("werkzeug")' instead.
#   "HTTP_USER_AGENT": f"werkzeug/{werkzeug.__version__}",
# 2023-11-20 21:13:40,258 INFO sqlalchemy.engine.Engine INSERT INTO users (first_name, last_name, image_url) VALUES (%(first_name)s, %(last_name)s, %(image_url)s) RETURNING users.id
# 2023-11-20 21:13:40,258 INFO sqlalchemy.engine.Engine [cached since 0.01223s ago] {'first_name': 'Lori', 'last_name': 'Litow', 'image_url': 'http://fakeprofilepic'}
# 2023-11-20 21:13:40,259 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,262 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,262 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# 2023-11-20 21:13:40,263 INFO sqlalchemy.engine.Engine [generated in 0.00036s] {}
# 2023-11-20 21:13:40,268 INFO sqlalchemy.engine.Engine ROLLBACK
# .2023-11-20 21:13:40,269 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,269 INFO sqlalchemy.engine.Engine DELETE FROM users
# 2023-11-20 21:13:40,270 INFO sqlalchemy.engine.Engine [cached since 0.02643s ago] {}
# 2023-11-20 21:13:40,270 INFO sqlalchemy.engine.Engine INSERT INTO users (first_name, last_name, image_url) VALUES (%(first_name)s, %(last_name)s, %(image_url)s) RETURNING users.id
# 2023-11-20 21:13:40,271 INFO sqlalchemy.engine.Engine [cached since 0.02516s ago] {'first_name': 'Paul', 'last_name': 'Pill', 'image_url': 'http://sample'}
# 2023-11-20 21:13:40,272 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,275 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,275 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,276 INFO sqlalchemy.engine.Engine [cached since 0.0247s ago] {'pk_1': 3}
# /home/lc131715/backend exercises springboard/sqlalchemy exercises/flask-blogly/app.py:94: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
#   user = User.query.get(user_id)
# 2023-11-20 21:13:40,279 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,279 INFO sqlalchemy.engine.Engine [generated in 0.00020s] {'pk_1': '3'}
# 2023-11-20 21:13:40,281 INFO sqlalchemy.engine.Engine UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, image_url=%(image_url)s WHERE users.id = %(users_id)s
# 2023-11-20 21:13:40,281 INFO sqlalchemy.engine.Engine [generated in 0.00020s] {'first_name': 'David', 'last_name': 'Schwartz', 'image_url': 'http://fakeprofilepic', 'users_id': 3}
# 2023-11-20 21:13:40,282 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,286 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,287 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# 2023-11-20 21:13:40,287 INFO sqlalchemy.engine.Engine [cached since 0.0245s ago] {}
# 2023-11-20 21:13:40,288 INFO sqlalchemy.engine.Engine ROLLBACK
# .2023-11-20 21:13:40,289 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,289 INFO sqlalchemy.engine.Engine DELETE FROM users
# 2023-11-20 21:13:40,289 INFO sqlalchemy.engine.Engine [cached since 0.0459s ago] {}
# 2023-11-20 21:13:40,290 INFO sqlalchemy.engine.Engine INSERT INTO users (first_name, last_name, image_url) VALUES (%(first_name)s, %(last_name)s, %(image_url)s) RETURNING users.id
# 2023-11-20 21:13:40,290 INFO sqlalchemy.engine.Engine [cached since 0.04499s ago] {'first_name': 'Paul', 'last_name': 'Pill', 'image_url': 'http://sample'}
# 2023-11-20 21:13:40,291 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,295 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,295 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,295 INFO sqlalchemy.engine.Engine [cached since 0.04428s ago] {'pk_1': 4}
# 2023-11-20 21:13:40,298 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,298 INFO sqlalchemy.engine.Engine [cached since 0.01911s ago] {'pk_1': '4'}
# 2023-11-20 21:13:40,300 INFO sqlalchemy.engine.Engine UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, image_url=%(image_url)s WHERE users.id = %(users_id)s
# 2023-11-20 21:13:40,300 INFO sqlalchemy.engine.Engine [cached since 0.01869s ago] {'first_name': 'David', 'last_name': 'Schwartz', 'image_url': 'http://fakeprofilepic', 'users_id': 4}
# 2023-11-20 21:13:40,301 INFO sqlalchemy.engine.Engine COMMIT
# .2023-11-20 21:13:40,304 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,305 INFO sqlalchemy.engine.Engine DELETE FROM users
# 2023-11-20 21:13:40,305 INFO sqlalchemy.engine.Engine [cached since 0.06155s ago] {}
# 2023-11-20 21:13:40,306 INFO sqlalchemy.engine.Engine INSERT INTO users (first_name, last_name, image_url) VALUES (%(first_name)s, %(last_name)s, %(image_url)s) RETURNING users.id
# 2023-11-20 21:13:40,307 INFO sqlalchemy.engine.Engine [cached since 0.06116s ago] {'first_name': 'Paul', 'last_name': 'Pill', 'image_url': 'http://sample'}
# 2023-11-20 21:13:40,308 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,311 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,311 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,311 INFO sqlalchemy.engine.Engine [cached since 0.06006s ago] {'pk_1': 5}
# /home/lc131715/backend exercises springboard/sqlalchemy exercises/flask-blogly/app.py:81: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
#   user = User.query.get(user_id )
# 2023-11-20 21:13:40,315 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,315 INFO sqlalchemy.engine.Engine [cached since 0.03589s ago] {'pk_1': '5'}
# 2023-11-20 21:13:40,317 INFO sqlalchemy.engine.Engine ROLLBACK
# .2023-11-20 21:13:40,319 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,319 INFO sqlalchemy.engine.Engine DELETE FROM users
# 2023-11-20 21:13:40,319 INFO sqlalchemy.engine.Engine [cached since 0.0761s ago] {}
# 2023-11-20 21:13:40,320 INFO sqlalchemy.engine.Engine INSERT INTO users (first_name, last_name, image_url) VALUES (%(first_name)s, %(last_name)s, %(image_url)s) RETURNING users.id
# 2023-11-20 21:13:40,321 INFO sqlalchemy.engine.Engine [cached since 0.07509s ago] {'first_name': 'Paul', 'last_name': 'Pill', 'image_url': 'http://sample'}
# 2023-11-20 21:13:40,321 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-20 21:13:40,325 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-20 21:13:40,325 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-11-20 21:13:40,325 INFO sqlalchemy.engine.Engine [cached since 0.07444s ago] {'pk_1': 6}
# 2023-11-20 21:13:40,328 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.image_url AS users_image_url
# FROM users
# 2023-11-20 21:13:40,328 INFO sqlalchemy.engine.Engine [cached since 0.06573s ago] {}
# 2023-11-20 21:13:40,329 INFO sqlalchemy.engine.Engine ROLLBACK
# .
# ----------------------------------------------------------------------
# Ran 5 tests in 0.089s

# OK










