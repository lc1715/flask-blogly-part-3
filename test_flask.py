from unittest import TestCase   
from app import app            
from models import db, User, Post     


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'  
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()              
db.create_all()             

class UserTestCase(TestCase):

    def setUp(self):           
        """Add sample user."""

        User.query.delete()     

        user = User(first_name='Paul', last_name='Pill', image_url='http://sample')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
       

    def tearDown(self):      
        """Clean up the session (db.session) in case there's any messed up savings in session (db.session)"""
        db.session.rollback()       

    def test_show_users(self):
        """Test the route '/users/' will show all users"""

        with app.test_client() as client:       
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



class PostTestCast(TestCase):
    def setUp(self):           
        """Add sample user."""

        Post.query.delete()   

        post = Post(title='Dogs', content='Love Dogs!', created_at='11-26-23')
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post
        
    def tearDown(self):      
        """Clean up the session (db.session) in case there's any messed up savings in session (db.session)"""
        db.session.rollback()       

    
    def test_show_posts(self):
        """Test the route '/posts/<int:post_id>' so that the post details will be
        shown to a user"""

        with app.test_client() as client:       
            resp= client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Dogs</h1>', html)
    
    
    def test_show_edit_post_form(self):
        """Test the route '/posts/<int:post_id>/edit' so that the edit post form 
        will be shown to the user"""

        with app.test_client() as client:       
            resp= client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Dogs', html)
    


