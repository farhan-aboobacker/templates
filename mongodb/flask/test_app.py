
import unittest
import json
from unittest.mock import patch, MagicMock
from app import app
from bson import ObjectId

class TestApp(unittest.TestCase):
    """Test suite for the Flask application."""

    def setUp(self):
        """Set up the test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.collection')
    def test_add_user_success(self, mock_collection):
        """Test successful user creation (POST /users)."""
        mock_collection.insert_one.return_value = MagicMock(inserted_id=ObjectId())
        user_data = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        response = self.app.post('/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {"message": "User added successfully!"})
        mock_collection.insert_one.assert_called_once_with(user_data)

    @patch('app.collection')
    def test_get_users(self, mock_collection):
        """Test retrieving all users (GET /users)."""
        users = [
            {'name': 'John Doe', 'email': 'john.doe@example.com'},
            {'name': 'Jane Doe', 'email': 'jane.doe@example.com'}
        ]
        mock_collection.find.return_value = users
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), users)
        mock_collection.find.assert_called_once_with({}, {'_id': False})

    @patch('app.collection')
    def test_get_user_by_id_success(self, mock_collection):
        """Test retrieving a single user by ID (GET /users/<id>)."""
        user_id = ObjectId()
        user = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        mock_collection.find_one.return_value = user
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), user)
        mock_collection.find_one.assert_called_once_with({'_id': user_id}, {'_id': False})

    @patch('app.collection')
    def test_get_user_by_id_not_found(self, mock_collection):
        """Test retrieving a non-existent user by ID (GET /users/<id>)."""
        user_id = ObjectId()
        mock_collection.find_one.return_value = None
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {"error": "User not found"})

    def test_get_user_by_id_invalid_id(self):
        """Test retrieving a user with an invalid ID format (GET /users/<id>)."""
        response = self.app.get('/users/invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Invalid ID"})

    @patch('app.collection')
    def test_update_user_by_id_success(self, mock_collection):
        """Test successfully updating a user by ID (PUT /users/<id>)."""
        user_id = ObjectId()
        update_data = {'name': 'John Doe Updated'}
        mock_collection.update_one.return_value = MagicMock(matched_count=1)
        response = self.app.put(f'/users/{user_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "User updated successfully!"})
        mock_collection.update_one.assert_called_once_with({'_id': user_id}, {'$set': update_data})

    @patch('app.collection')
    def test_update_user_by_id_not_found(self, mock_collection):
        """Test updating a non-existent user by ID (PUT /users/<id>)."""
        user_id = ObjectId()
        update_data = {'name': 'John Doe Updated'}
        mock_collection.update_one.return_value = MagicMock(matched_count=0)
        response = self.app.put(f'/users/{user_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {"error": "User not found"})

    def test_update_user_by_id_invalid_id(self):
        """Test updating a user with an invalid ID format (PUT /users/<id>)."""
        update_data = {'name': 'John Doe Updated'}
        response = self.app.put('/users/invalid_id', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Invalid ID"})

    @patch('app.collection')
    def test_delete_user_by_id_success(self, mock_collection):
        """Test successfully deleting a user by ID (DELETE /users/<id>)."""
        user_id = ObjectId()
        mock_collection.delete_one.return_value = MagicMock(deleted_count=1)
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "User deleted successfully!"})
        mock_collection.delete_one.assert_called_once_with({'_id': user_id})

    @patch('app.collection')
    def test_delete_user_by_id_not_found(self, mock_collection):
        """Test deleting a non-existent user by ID (DELETE /users/<id>)."""
        user_id = ObjectId()
        mock_collection.delete_one.return_value = MagicMock(deleted_count=0)
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {"error": "User not found"})

    def test_delete_user_by_id_invalid_id(self):
        """Test deleting a user with an invalid ID format (DELETE /users/<id>)."""
        response = self.app.delete('/users/invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Invalid ID"})

if __name__ == "__main__":
    unittest.main()