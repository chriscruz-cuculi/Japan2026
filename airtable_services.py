"""
Airtable Services Module
Handles interactions with Airtable API for message uploads and data management.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import os


class AirtableService:
    """Service class for interacting with Airtable API."""
    
    def __init__(self, api_key: Optional[str] = None, base_id: Optional[str] = None):
        """
        Initialize Airtable service.
        
        Args:
            api_key: Airtable API key (defaults to AIRTABLE_API_KEY env var)
            base_id: Airtable base ID (defaults to AIRTABLE_BASE_ID env var)
        """
        self.api_key = api_key or os.getenv('AIRTABLE_API_KEY')
        self.base_id = base_id or os.getenv('AIRTABLE_BASE_ID')
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}"
        
        if not self.api_key:
            raise ValueError("Airtable API key is required")
        if not self.base_id:
            raise ValueError("Airtable base ID is required")
    
    def message_upload(
        self,
        table_name: str,
        message: str,
        event_date: Optional[str] = None,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        message_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Upload a message to Airtable with event_date support.
        
        Args:
            table_name: Name of the Airtable table
            message: The message content to upload
            event_date: Date of the event (ISO format: YYYY-MM-DD or datetime object)
            sender: Sender identifier
            recipient: Recipient identifier
            message_type: Type/category of message
            metadata: Additional metadata as dictionary
            **kwargs: Additional fields to include in the record
            
        Returns:
            Dict containing the created record information
            
        Example:
            >>> service = AirtableService()
            >>> result = service.message_upload(
            ...     table_name="Messages",
            ...     message="Meeting scheduled",
            ...     event_date="2025-04-05",
            ...     sender="user@example.com",
            ...     message_type="notification"
            ... )
        """
        # Format event_date if it's a datetime object
        if isinstance(event_date, datetime):
            event_date = event_date.strftime('%Y-%m-%d')
        
        # Build the record fields
        fields = {
            "Message": message,
        }
        
        # Add event_date if provided
        if event_date:
            fields["EventDate"] = event_date
        
        # Add optional fields if provided
        if sender:
            fields["Sender"] = sender
        if recipient:
            fields["Recipient"] = recipient
        if message_type:
            fields["MessageType"] = message_type
        if metadata:
            fields["Metadata"] = str(metadata)
        
        # Add any additional fields from kwargs
        fields.update(kwargs)
        
        # Prepare the request payload
        payload = {
            "records": [
                {
                    "fields": fields
                }
            ]
        }
        
        # In a real implementation, this would make an HTTP request
        # For now, return a mock successful response
        from datetime import timezone
        return {
            "id": "recXXXXXXXXXXXXXX",
            "fields": fields,
            "createdTime": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
    
    def message_upload_batch(
        self,
        table_name: str,
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Upload multiple messages to Airtable in batch.
        
        Args:
            table_name: Name of the Airtable table
            messages: List of message dictionaries, each containing:
                - message: The message content (required)
                - event_date: Date of the event (optional)
                - Other optional fields
                
        Returns:
            List of created record information
            
        Example:
            >>> service = AirtableService()
            >>> results = service.message_upload_batch(
            ...     table_name="Messages",
            ...     messages=[
            ...         {
            ...             "message": "Event 1",
            ...             "event_date": "2025-04-03",
            ...             "sender": "user1@example.com"
            ...         },
            ...         {
            ...             "message": "Event 2",
            ...             "event_date": "2025-04-05",
            ...             "sender": "user2@example.com"
            ...         }
            ...     ]
            ... )
        """
        results = []
        
        for msg_data in messages:
            message = msg_data.pop('message', None)
            if not message:
                continue
                
            result = self.message_upload(
                table_name=table_name,
                message=message,
                **msg_data
            )
            results.append(result)
        
        return results
    
    def get_messages_by_event_date(
        self,
        table_name: str,
        event_date: str,
        filter_formula: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve messages filtered by event_date.
        
        Args:
            table_name: Name of the Airtable table
            event_date: Event date to filter by (YYYY-MM-DD format)
            filter_formula: Optional additional Airtable filter formula
            
        Returns:
            List of records matching the event_date
        """
        # Build filter formula
        base_filter = f"{{EventDate}}='{event_date}'"
        
        if filter_formula:
            combined_filter = f"AND({base_filter},{filter_formula})"
        else:
            combined_filter = base_filter
        
        # In a real implementation, this would make an HTTP GET request
        # with the filter formula as a parameter
        return []
    
    def update_message_event_date(
        self,
        table_name: str,
        record_id: str,
        new_event_date: str
    ) -> Dict[str, Any]:
        """
        Update the event_date for an existing message record.
        
        Args:
            table_name: Name of the Airtable table
            record_id: Airtable record ID
            new_event_date: New event date (YYYY-MM-DD format)
            
        Returns:
            Updated record information
        """
        # Format event_date if it's a datetime object
        if isinstance(new_event_date, datetime):
            new_event_date = new_event_date.strftime('%Y-%m-%d')
        
        # In a real implementation, this would make an HTTP PATCH request
        return {
            "id": record_id,
            "fields": {
                "EventDate": new_event_date
            }
        }


# Convenience function for quick message uploads
def quick_message_upload(
    message: str,
    event_date: Optional[str] = None,
    table_name: str = "Messages",
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function for quick message uploads with event_date.
    
    Args:
        message: The message content
        event_date: Optional event date (YYYY-MM-DD format)
        table_name: Airtable table name (default: "Messages")
        **kwargs: Additional fields
        
    Returns:
        Created record information
    """
    service = AirtableService()
    return service.message_upload(
        table_name=table_name,
        message=message,
        event_date=event_date,
        **kwargs
    )
