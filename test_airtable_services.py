"""
Unit tests for airtable_services.py
Tests event_date functionality and backward compatibility
"""

import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from airtable_services import AirtableService, quick_message_upload


class TestAirtableServiceEventDate(unittest.TestCase):
    """Test suite for event_date functionality in message_upload"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.service = AirtableService(
            api_key="test_api_key",
            base_id="test_base_id"
        )
    
    def test_message_upload_with_string_event_date(self):
        """Test message_upload with event_date as string"""
        result = self.service.message_upload(
            table_name="Messages",
            message="Test message",
            event_date="2025-04-05",
            sender="test@example.com"
        )
        
        self.assertIn("id", result)
        self.assertIn("fields", result)
        self.assertEqual(result["fields"]["EventDate"], "2025-04-05")
        self.assertEqual(result["fields"]["Message"], "Test message")
    
    def test_message_upload_with_datetime_event_date(self):
        """Test message_upload with event_date as datetime object"""
        event = datetime(2025, 4, 5, 10, 30)
        
        result = self.service.message_upload(
            table_name="Messages",
            message="Test with datetime",
            event_date=event
        )
        
        self.assertEqual(result["fields"]["EventDate"], "2025-04-05")
    
    def test_message_upload_without_event_date(self):
        """Test backward compatibility - upload without event_date"""
        result = self.service.message_upload(
            table_name="Messages",
            message="Test without event_date",
            sender="test@example.com"
        )
        
        self.assertIn("id", result)
        self.assertIn("fields", result)
        self.assertEqual(result["fields"]["Message"], "Test without event_date")
        self.assertNotIn("EventDate", result["fields"])
    
    def test_message_upload_with_all_parameters(self):
        """Test message_upload with all parameters including event_date"""
        result = self.service.message_upload(
            table_name="Messages",
            message="Complete test",
            event_date="2025-04-05",
            sender="sender@example.com",
            recipient="recipient@example.com",
            message_type="test",
            metadata={"priority": "high", "tags": ["important"]}
        )
        
        fields = result["fields"]
        self.assertEqual(fields["Message"], "Complete test")
        self.assertEqual(fields["EventDate"], "2025-04-05")
        self.assertEqual(fields["Sender"], "sender@example.com")
        self.assertEqual(fields["Recipient"], "recipient@example.com")
        self.assertEqual(fields["MessageType"], "test")
        self.assertIn("Metadata", fields)
    
    def test_message_upload_batch_with_event_dates(self):
        """Test batch upload with multiple event_dates"""
        messages = [
            {
                "message": "Message 1",
                "event_date": "2025-04-03",
                "sender": "user1"
            },
            {
                "message": "Message 2",
                "event_date": "2025-04-05",
                "sender": "user2"
            },
            {
                "message": "Message 3",
                "event_date": "2025-04-07",
                "sender": "user3"
            }
        ]
        
        results = self.service.message_upload_batch(
            table_name="Messages",
            messages=messages
        )
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["fields"]["EventDate"], "2025-04-03")
        self.assertEqual(results[1]["fields"]["EventDate"], "2025-04-05")
        self.assertEqual(results[2]["fields"]["EventDate"], "2025-04-07")
    
    def test_message_upload_batch_mixed_event_dates(self):
        """Test batch upload with some messages having event_dates and others not"""
        messages = [
            {
                "message": "With date",
                "event_date": "2025-04-05"
            },
            {
                "message": "Without date",
                "sender": "test"
            }
        ]
        
        results = self.service.message_upload_batch(
            table_name="Messages",
            messages=messages
        )
        
        self.assertEqual(len(results), 2)
        self.assertIn("EventDate", results[0]["fields"])
        self.assertNotIn("EventDate", results[1]["fields"])
    
    def test_update_message_event_date_with_string(self):
        """Test updating event_date with string"""
        result = self.service.update_message_event_date(
            table_name="Messages",
            record_id="recTEST123",
            new_event_date="2025-04-10"
        )
        
        self.assertEqual(result["id"], "recTEST123")
        self.assertEqual(result["fields"]["EventDate"], "2025-04-10")
    
    def test_update_message_event_date_with_datetime(self):
        """Test updating event_date with datetime object"""
        new_date = datetime(2025, 4, 15, 9, 0)
        
        result = self.service.update_message_event_date(
            table_name="Messages",
            record_id="recTEST456",
            new_event_date=new_date
        )
        
        self.assertEqual(result["fields"]["EventDate"], "2025-04-15")
    
    def test_quick_message_upload_with_event_date(self):
        """Test convenience function with event_date"""
        with patch('airtable_services.AirtableService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            mock_instance.message_upload.return_value = {
                "id": "recQUICK",
                "fields": {"Message": "Quick test", "EventDate": "2025-04-05"}
            }
            
            result = quick_message_upload(
                message="Quick test",
                event_date="2025-04-05",
                message_type="test"
            )
            
            mock_instance.message_upload.assert_called_once()
    
    def test_get_messages_by_event_date(self):
        """Test querying messages by event_date"""
        messages = self.service.get_messages_by_event_date(
            table_name="Messages",
            event_date="2025-04-05"
        )
        
        # Should return a list (empty in mock implementation)
        self.assertIsInstance(messages, list)
    
    def test_message_upload_with_custom_fields(self):
        """Test that additional kwargs work alongside event_date"""
        result = self.service.message_upload(
            table_name="Messages",
            message="Custom fields test",
            event_date="2025-04-05",
            custom_field_1="value1",
            custom_field_2="value2",
            priority=5
        )
        
        fields = result["fields"]
        self.assertEqual(fields["EventDate"], "2025-04-05")
        self.assertEqual(fields["custom_field_1"], "value1")
        self.assertEqual(fields["custom_field_2"], "value2")
        self.assertEqual(fields["priority"], 5)


class TestAirtableServiceInitialization(unittest.TestCase):
    """Test service initialization and configuration"""
    
    def test_initialization_with_params(self):
        """Test initialization with explicit parameters"""
        service = AirtableService(
            api_key="test_key",
            base_id="test_base"
        )
        
        self.assertEqual(service.api_key, "test_key")
        self.assertEqual(service.base_id, "test_base")
        self.assertIn("test_base", service.base_url)
    
    @patch.dict('os.environ', {
        'AIRTABLE_API_KEY': 'env_key',
        'AIRTABLE_BASE_ID': 'env_base'
    })
    def test_initialization_from_env(self):
        """Test initialization from environment variables"""
        service = AirtableService()
        
        self.assertEqual(service.api_key, "env_key")
        self.assertEqual(service.base_id, "env_base")
    
    def test_initialization_missing_api_key(self):
        """Test that missing API key raises error"""
        with self.assertRaises(ValueError) as context:
            AirtableService(api_key=None, base_id="test_base")
        
        self.assertIn("API key", str(context.exception))
    
    def test_initialization_missing_base_id(self):
        """Test that missing base ID raises error"""
        with self.assertRaises(ValueError) as context:
            AirtableService(api_key="test_key", base_id=None)
        
        self.assertIn("base ID", str(context.exception))


class TestEventDateFormats(unittest.TestCase):
    """Test various event_date format scenarios"""
    
    def setUp(self):
        self.service = AirtableService(
            api_key="test_key",
            base_id="test_base"
        )
    
    def test_event_date_iso_format(self):
        """Test ISO format date (YYYY-MM-DD)"""
        result = self.service.message_upload(
            table_name="Messages",
            message="ISO date",
            event_date="2025-04-05"
        )
        
        self.assertEqual(result["fields"]["EventDate"], "2025-04-05")
    
    def test_event_date_datetime_midnight(self):
        """Test datetime at midnight"""
        event = datetime(2025, 4, 5, 0, 0, 0)
        
        result = self.service.message_upload(
            table_name="Messages",
            message="Midnight event",
            event_date=event
        )
        
        self.assertEqual(result["fields"]["EventDate"], "2025-04-05")
    
    def test_event_date_datetime_with_time(self):
        """Test datetime with time (should use date only)"""
        event = datetime(2025, 4, 5, 14, 30, 45)
        
        result = self.service.message_upload(
            table_name="Messages",
            message="Timed event",
            event_date=event
        )
        
        self.assertEqual(result["fields"]["EventDate"], "2025-04-05")
    
    def test_event_date_none(self):
        """Test explicit None for event_date"""
        result = self.service.message_upload(
            table_name="Messages",
            message="No date",
            event_date=None
        )
        
        self.assertNotIn("EventDate", result["fields"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
