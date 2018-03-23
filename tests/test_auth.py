import unittest
import json

# local import
from app import create_app

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'email': 'test@example.com',
            'password': 'test_password'
        }

    def test_registration(self):
        # Test user registration works correcty.
        resp = self.client().post('/api/auth/register', data=self.user_data)
        result = json.loads(resp.data.decode())
        self.assertEqual(
            result['message'], "You registered successfully. Please login.")
        self.assertEqual(resp.status_code, 201)

    def test_already_registered_user(self):
        # Test that a user cannot be registered twice.
        resp = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        second_res = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please login.")

    def test_user_login(self):
        # Test registered user can login.
        resp = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        login_resp = self.client().post('/api/auth/login', data=self.user_data)
        result = json.loads(login_resp.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_resp.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        # Test non registered users cannot login
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        resp = self.client().post('/api/auth/login', data=not_a_user)
        result = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again.")
    
    def test_user_logout(self):
        # Test registered user can logout.
        resp = self.client().post('/api/auth/logout', data=self.user_data)
        result = json.loads(resp.data.decode())
        self.assertEqual(
            result['message'], "You have successfully logged out.")
        self.assertEqual(resp.status_code, 200)