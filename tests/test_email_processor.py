import pytest
from src.email_processor import EmailProcessor

def test_valid_email_processing():
    processor = EmailProcessor()
    
    test_email = {
        'subject': 'Technical Issue',
        'body': 'Having problems with login',
        'sender': 'test@example.com'
    }
    
    result = processor.process_email(test_email)
    assert result['success']
    assert 'category' in result
    assert 'confidence' in result
    assert 'response' in result

def test_invalid_email():
    processor = EmailProcessor()
    
    test_email = {
        'subject': 'Test',
        'body': 'Test message',
        'sender': 'invalid-email'
    }
    
    result = processor.process_email(test_email)
    assert not result['success']
    assert 'error' in result 