import unittest
from flask import Flask
from website.auth import auth
from website.models import User
from werkzeug.security import generate_password_hash
from website import db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SECRET_KEY'] = 'secret'
        db.init_app(self.app)
        self.app.register_blueprint(auth)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(email='test@example.com', name='Test User', password=generate_password_hash('password123', method='sha256'))
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_sign_up_get(self):
        response = self.client.get('/sign-up')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up', response.data)

    def test_sign_up_post(self):
        response = self.client.post('/sign-up', data={
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'Password123!',
            'confirmedPassword': 'Password123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User registered successfully', response.data)

    def test_sign_up_post_invalid_email(self):
        response = self.client.post('/sign-up', data={
            'name': 'New User',
            'email': 'invalid-email',
            'password': 'Password123!',
            'confirmedPassword': 'Password123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)

    def test_sign_up_post_invalid_password(self):
        response = self.client.post('/sign-up', data={
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'pass',
            'confirmedPassword': 'pass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password must be at least 8 characters long', response.data)

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log in', response.data)

    def test_login_post(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data)

    def test_login_post_invalid_credentials(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)

    def test_logout(self):
        with self.client:
            self.client.post('/login', data={
                'email': 'test@example.com',
                'password': 'password123'
            })
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Logout Page', response.data)

if __name__ == '__main__':
    unittest.main()