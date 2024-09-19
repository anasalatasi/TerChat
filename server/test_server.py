import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app import app, socketio, get_cached_message_count, clear_cache_periodically
from db_service import DatabaseService
from werkzeug.exceptions import BadRequest
import json
class TestServer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    @patch('app.DatabaseService.insert_message')
    @patch('app.socketio.emit')
    def test_send_message(self, mock_emit, mock_insert):
        data = {'text': 'Test message', 'sender': 'Test User'}
        response = self.app.post('/messages', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'status': 'Message received'})
        mock_insert.assert_called_once()
        mock_emit.assert_called_once()
        
    def test_send_message_missing_text(self):
        data = {'sender': 'Test User'}
        response = self.app.post('/messages', json=data)
        self.assertEqual(response.status_code, 400)
        
    @patch('app.DatabaseService.get_all_messages')
    def test_get_messages(self, mock_get_all):
        mock_get_all.return_value = [{'text': 'Test', 'timestamp': '2023-04-14T12:00:00', 'sender': 'User'}]
        response = self.app.get('/messages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_get_all.return_value)
        
    @patch('app.get_cached_message_count')
    def test_message_count(self, mock_get_count):
        mock_get_count.return_value = 5
        response = self.app.get('/messages/count')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'count': 5})
        
    @patch('app.DatabaseService.get_message_count')
    def test_get_cached_message_count(self, mock_get_count):
        mock_get_count.return_value = 10
        result = get_cached_message_count()
        self.assertEqual(result, 10)
        # Call again to test caching
        get_cached_message_count()
        mock_get_count.assert_called_once()
        
    def test_clear_cache_periodically(self):
        with patch('app.time') as mock_time, \
             patch('app.clear_message_count_cache') as mock_clear_cache:
            mock_time.return_value = 100
            clear_cache_periodically.last_clear = 97
            clear_cache_periodically()
            mock_clear_cache.assert_called_once()
            # Test when time difference is less than 2 seconds
            mock_time.return_value = 98
            clear_cache_periodically.last_clear = 97
            clear_cache_periodically()
            mock_clear_cache.assert_called_once()  # Should not be called again
            
    @patch('app.print')
    def test_handle_connect(self, mock_print):
        with app.test_request_context('/'):
            socketio.test_client(app).connect()
            mock_print.assert_called_with('Client connected')
            
    @patch('app.print')
    def test_handle_disconnect(self, mock_print):
        with app.test_request_context('/'):
            client = socketio.test_client(app)
            client.connect()
            client.disconnect()
            mock_print.assert_called_with('Client disconnected')
            
    @patch('app.DatabaseService.init_db')
    @patch('app.socketio.run')
    def test_run_server(self, mock_run, mock_init_db):
        from app import run_server
        run_server()
        mock_init_db.assert_called_once()
        mock_run.assert_called_once_with(app, host='0.0.0.0', port=5005, allow_unsafe_werkzeug=True)
        
if __name__ == '__main__':
    unittest.main()