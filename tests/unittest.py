import unittest
from unittest.mock import patch, Mock
from main import app

class TestAPIWithMocks(unittest.TestCase):

    @patch('app.create_access_token', return_value='fake_token')
    @patch('app.request')
    def test_login_with_mock(self, mock_request, mock_create_access_token):
        mock_request.form = {'username' : 'username1', 'password' : 'password1'}
        mock_request.method = 'POST'
        mock_request.status_code = 200

        with app.test_client() as client:
            response = client.post('/login')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['access_token'], 'fake_token')

if __name__ == '__main__':
    unittest.main()