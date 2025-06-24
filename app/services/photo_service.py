"""
Photo service for BOA API.

This module handles photo retrieval from the mock database.
In production, this would interface with the actual RDW database.
"""

import base64
from typing import Tuple, Optional
import asyncio
from app.utils.exceptions import PhotoNotFoundError

# Mock photo database - In production, this would be replaced with actual database queries
MOCK_PHOTO_DATABASE = {
    # BSN -> {birth_date -> (photo_data, photo_id)}
    "123456782": {  # Valid BSN for testing
        "2000-08-16": ("/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=", 1),
        "1995-00-00": ("/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCAACAAIDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=", 2)
    },
    "987654329": {  # Another valid BSN for testing
        "1985-12-25": ("/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCAADAAMDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=", 3)
    },
    "147258369": {  # Third valid BSN for testing
        "1990-05-10": ("/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCAAEAAQDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=", 4)
    }
}


async def get_photo_by_criteria(bsn: str, birth_date: str) -> Tuple[str, int]:
    """
    Retrieve photo data based on BSN and birth date.
    
    This is a mock implementation that simulates database lookup.
    In production, this would query the actual RDW database.
    
    Args:
        bsn (str): Valid 9-digit BSN
        birth_date (str): Birth date in ISO 8601 format
        
    Returns:
        Tuple[str, int]: Base64 encoded photo data and photo ID
        
    Raises:
        PhotoNotFoundError: If no photo is found for the given criteria
        
    Example:
        >>> photo_data, photo_id = await get_photo_by_criteria("123456782", "2000-08-16")
        >>> print(f"Found photo with ID: {photo_id}")
    """
    # Simulate database query delay
    await asyncio.sleep(0.1)
    
    # Check if BSN exists in mock database
    if bsn not in MOCK_PHOTO_DATABASE:
        raise PhotoNotFoundError(bsn, birth_date)
    
    # Check if birth date exists for this BSN
    bsn_records = MOCK_PHOTO_DATABASE[bsn]
    if birth_date not in bsn_records:
        raise PhotoNotFoundError(bsn, birth_date)
    
    # Return photo data and ID
    photo_data, photo_id = bsn_records[birth_date]
    return photo_data, photo_id


async def get_photo_by_id(photo_id: int) -> Optional[str]:
    """
    Retrieve photo data by photo ID.
    
    This is a helper function for direct photo lookup by ID.
    
    Args:
        photo_id (int): Photo ID to search for
        
    Returns:
        Optional[str]: Base64 encoded photo data if found, None otherwise
    """
    # Simulate database query delay
    await asyncio.sleep(0.1)
    
    # Search through all records to find photo by ID
    for bsn_records in MOCK_PHOTO_DATABASE.values():
        for photo_data, pid in bsn_records.values():
            if pid == photo_id:
                return photo_data
    
    return None


def add_mock_photo(bsn: str, birth_date: str, photo_data: str, photo_id: int) -> bool:
    """
    Add a mock photo to the database for testing.
    
    This function is used for testing purposes to add additional photos
    to the mock database.
    
    Args:
        bsn (str): BSN for the photo
        birth_date (str): Birth date for the photo
        photo_data (str): Base64 encoded photo data
        photo_id (int): Unique photo ID
        
    Returns:
        bool: True if photo was added successfully
    """
    if bsn not in MOCK_PHOTO_DATABASE:
        MOCK_PHOTO_DATABASE[bsn] = {}
    
    MOCK_PHOTO_DATABASE[bsn][birth_date] = (photo_data, photo_id)
    return True


def get_database_stats() -> dict:
    """
    Get statistics about the mock photo database.
    
    Returns:
        dict: Database statistics including counts and BSN list
    """
    total_bsn_count = len(MOCK_PHOTO_DATABASE)
    total_photo_count = sum(
        len(records) for records in MOCK_PHOTO_DATABASE.values()
    )
    
    return {
        "total_bsn_records": total_bsn_count,
        "total_photos": total_photo_count,
        "available_bsns": list(MOCK_PHOTO_DATABASE.keys()),
        "database_type": "mock"
    }


def create_sample_photo_base64() -> str:
    """
    Create a minimal sample photo in base64 format.
    
    This creates a tiny 1x1 pixel JPEG image for testing purposes.
    
    Returns:
        str: Base64 encoded sample photo
    """
    # Minimal 1x1 pixel JPEG in base64
    # This is a valid JPEG image that can be decoded and displayed
    return "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
