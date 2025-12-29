"""
Example usage of airtable_services.py with event_date support
"""

from datetime import datetime
from airtable_services import AirtableService, quick_message_upload


def example_basic_upload():
    """Example: Basic message upload with event_date"""
    service = AirtableService(
        api_key="your_api_key_here",
        base_id="your_base_id_here"
    )
    
    # Upload a message with event_date as string
    result = service.message_upload(
        table_name="Messages",
        message="Trip planning meeting scheduled",
        event_date="2025-04-03",
        sender="coordinator@example.com",
        message_type="planning"
    )
    
    print(f"Message uploaded: {result['id']}")
    print(f"Event Date: {result['fields']['EventDate']}")


def example_datetime_upload():
    """Example: Upload with datetime object"""
    service = AirtableService()
    
    # Use datetime object - will be automatically converted
    event = datetime(2025, 4, 5, 10, 30)
    
    result = service.message_upload(
        table_name="Messages",
        message="Cherry blossom viewing at Ueno Park",
        event_date=event,
        sender="travel_bot",
        recipient="group_chat",
        message_type="itinerary"
    )
    
    print(f"Uploaded with datetime: {result['fields']['EventDate']}")


def example_batch_upload():
    """Example: Batch upload multiple messages with event_dates"""
    service = AirtableService()
    
    # Upload multiple messages for different dates
    messages = [
        {
            "message": "Arrival in Tokyo",
            "event_date": "2025-04-03",
            "sender": "system",
            "message_type": "arrival"
        },
        {
            "message": "Senso-ji Temple visit",
            "event_date": "2025-04-04",
            "sender": "itinerary_bot",
            "message_type": "activity"
        },
        {
            "message": "Shinkansen to Kyoto",
            "event_date": "2025-04-07",
            "sender": "itinerary_bot",
            "message_type": "transportation"
        }
    ]
    
    results = service.message_upload_batch(
        table_name="Messages",
        messages=messages
    )
    
    print(f"Batch uploaded {len(results)} messages")


def example_backward_compatibility():
    """Example: Upload without event_date (backward compatible)"""
    service = AirtableService()
    
    # This still works - event_date is optional
    result = service.message_upload(
        table_name="Messages",
        message="General reminder about luggage service",
        sender="admin",
        message_type="reminder"
    )
    
    print(f"Upload without event_date works: {result['id']}")


def example_quick_upload():
    """Example: Using convenience function"""
    # Quick upload with event_date
    result = quick_message_upload(
        message="teamLab Planets tickets confirmed",
        event_date="2025-04-05",
        message_type="confirmation"
    )
    
    print(f"Quick upload successful: {result['id']}")


def example_query_by_date():
    """Example: Query messages by event_date"""
    service = AirtableService()
    
    # Get all messages for a specific date
    messages = service.get_messages_by_event_date(
        table_name="Messages",
        event_date="2025-04-05"
    )
    
    print(f"Found {len(messages)} messages for April 5th")


def example_update_event_date():
    """Example: Update event_date on existing record"""
    service = AirtableService()
    
    # Change the event date for a message
    result = service.update_message_event_date(
        table_name="Messages",
        record_id="recXXXXXXXXXXXXXX",
        new_event_date="2025-04-06"
    )
    
    print(f"Updated event date: {result['fields']['EventDate']}")


if __name__ == "__main__":
    print("Airtable Services - event_date Examples\n")
    print("=" * 50)
    
    # Note: These examples will work once you set up:
    # - AIRTABLE_API_KEY environment variable
    # - AIRTABLE_BASE_ID environment variable
    # Or pass them directly to AirtableService()
    
    print("\n1. Basic Upload with event_date:")
    print("   service.message_upload(..., event_date='2025-04-03')")
    
    print("\n2. DateTime Object:")
    print("   event_date=datetime(2025, 4, 5)")
    
    print("\n3. Batch Upload:")
    print("   service.message_upload_batch(...)")
    
    print("\n4. Backward Compatible:")
    print("   message_upload() works without event_date")
    
    print("\n5. Query by Date:")
    print("   service.get_messages_by_event_date(...)")
    
    print("\n" + "=" * 50)
    print("All examples maintain compatibility with existing code!")
