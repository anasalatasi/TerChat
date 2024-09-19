import unittest
from unittest.mock import patch
from server.app import app, get_cached_message_count, clear_cache_periodically
import json


class TestServer(unittest.TestCase):

    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    @patch("server.app.DatabaseService.insert_message")
    @patch("server.app.socketio.emit")
    def test_send_message_success(self, mock_emit, mock_insert_message):
        # Simulate a POST request to the /messages endpoint
        data = {"text": "Hello, world!", "sender": "test_user"}
        response = self.app.post("/messages", json=data)

        # Ensure the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Ensure the JSON response is correct
        self.assertEqual(json.loads(response.data), {"status": "Message received"})

        # Check that the database insertion and socket emit were called
        mock_insert_message.assert_called_once_with(
            "Hello, world!", unittest.mock.ANY, "test_user"
        )
        mock_emit.assert_called_once_with("new_message", unittest.mock.ANY)

    def test_send_message_missing_text(self):
        # Simulate a POST request with missing 'text'
        data = {"sender": "test_user"}
        response = self.app.post("/messages", json=data)

        # Ensure the response status is 400 Bad Request
        self.assertEqual(response.status_code, 400)

    @patch("server.app.DatabaseService.get_all_messages")
    def test_get_messages(self, mock_get_all_messages):
        # Mock the response from the database
        mock_get_all_messages.return_value = [
            {
                "text": "Test message",
                "timestamp": "2024-09-20T12:00:00",
                "sender": "test_user",
            }
        ]

        # Simulate a GET request to the /messages endpoint
        response = self.app.get("/messages")

        # Ensure the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Ensure the JSON response is correct
        expected_response = [
            {
                "text": "Test message",
                "timestamp": "2024-09-20T12:00:00",
                "sender": "test_user",
            }
        ]
        self.assertEqual(json.loads(response.data), expected_response)

        # Check that the database query was called
        mock_get_all_messages.assert_called_once()

    @patch("server.app.get_cached_message_count")
    def test_message_count(self, mock_get_cached_message_count):
        # Mock the cached message count
        mock_get_cached_message_count.return_value = 5

        # Simulate a GET request to the /messages/count endpoint
        response = self.app.get("/messages/count")

        # Ensure the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Ensure the JSON response contains the correct count
        self.assertEqual(json.loads(response.data), {"count": 5})

        # Check that the cached message count function was called
        mock_get_cached_message_count.assert_called_once()

    @patch("server.app.clear_message_count_cache")
    @patch("server.app.time")
    def test_clear_cache_periodically(self, mock_time, mock_clear_message_count_cache):
        # Set up the mock time to simulate periodic cache clearing
        mock_time.return_value = 100
        clear_cache_periodically.last_clear = 97

        # Call the function to clear the cache periodically
        clear_cache_periodically()

        # Check that the cache clearing function was called
        mock_clear_message_count_cache.assert_called_once()

        # Check that the cache wasn't cleared if the time hasn't exceeded 2 seconds
        mock_time.return_value = 98
        clear_cache_periodically.last_clear = 97
        clear_cache_periodically()
        mock_clear_message_count_cache.assert_called_once()  # Should still be called only once


if __name__ == "__main__":
    unittest.main()
