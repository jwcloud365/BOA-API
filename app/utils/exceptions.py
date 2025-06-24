"""
Custom exceptions for BOA API.

This module defines custom exception classes for different types of
errors that can occur in the BOA API application.
"""


class BOABaseException(Exception):
    """Base exception for all BOA API exceptions."""
    
    def __init__(self, message: str, error_code: str = None):
        """
        Initialize BOA base exception.
        
        Args:
            message (str): Error message
            error_code (str, optional): Error code for categorization
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class BOAValidationError(BOABaseException):
    """Exception raised for validation errors."""
    
    def __init__(self, field: str, message: str, value=None):
        """
        Initialize validation error.
        
        Args:
            field (str): Field that failed validation
            message (str): Validation error message
            value: The invalid value (optional)
        """
        self.field = field
        self.value = value
        full_message = f"Validation error for field '{field}': {message}"
        if value is not None:
            full_message += f" (received: {value})"
        super().__init__(full_message, "VALIDATION_ERROR")


class BSNValidationError(BOAValidationError):
    """Exception raised for BSN validation errors."""
    
    def __init__(self, bsn: str, reason: str):
        """
        Initialize BSN validation error.
        
        Args:
            bsn (str): The invalid BSN
            reason (str): Reason for validation failure
        """
        super().__init__(
            field="BSN",
            message=f"Invalid BSN: {reason}",
            value=bsn
        )


class DateValidationError(BOAValidationError):
    """Exception raised for date validation errors."""
    
    def __init__(self, date_value: str, reason: str):
        """
        Initialize date validation error.
        
        Args:
            date_value (str): The invalid date value
            reason (str): Reason for validation failure
        """
        super().__init__(
            field="geboortedatum",
            message=f"Invalid date format: {reason}",
            value=date_value
        )


class PublicKeyValidationError(BOAValidationError):
    """Exception raised for public key validation errors."""
    
    def __init__(self, reason: str, key_data=None):
        """
        Initialize public key validation error.
        
        Args:
            reason (str): Reason for validation failure
            key_data: The invalid key data (optional)
        """
        super().__init__(
            field="ontvanger-publieke-sleutel",
            message=f"Invalid public key: {reason}",
            value=key_data
        )


class BOANotFoundError(BOABaseException):
    """Exception raised when requested resource is not found."""
    
    def __init__(self, resource_type: str, criteria: str = None):
        """
        Initialize not found error.
        
        Args:
            resource_type (str): Type of resource not found
            criteria (str, optional): Search criteria used
        """
        message = f"{resource_type} not found"
        if criteria:
            message += f" for criteria: {criteria}"
        super().__init__(message, "NOT_FOUND")


class PhotoNotFoundError(BOANotFoundError):
    """Exception raised when photo is not found."""
    
    def __init__(self, bsn: str, birth_date: str):
        """
        Initialize photo not found error.
        
        Args:
            bsn (str): BSN that was searched
            birth_date (str): Birth date that was searched
        """
        super().__init__(
            resource_type="Photo",
            criteria=f"BSN: {bsn}, Birth date: {birth_date}"
        )


class EncryptionError(BOABaseException):
    """Exception raised for encryption/decryption errors."""
    
    def __init__(self, operation: str, reason: str):
        """
        Initialize encryption error.
        
        Args:
            operation (str): Encryption operation that failed
            reason (str): Reason for failure
        """
        super().__init__(
            message=f"Encryption {operation} failed: {reason}",
            error_code="ENCRYPTION_ERROR"
        )


class PhotoProcessingError(BOABaseException):
    """Exception raised for photo processing errors."""
    
    def __init__(self, operation: str, reason: str):
        """
        Initialize photo processing error.
        
        Args:
            operation (str): Photo operation that failed
            reason (str): Reason for failure
        """
        super().__init__(
            message=f"Photo {operation} failed: {reason}",
            error_code="PHOTO_PROCESSING_ERROR"
        )
