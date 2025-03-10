from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
import logging

from .models.classifier import EmailClassifier
from .models.response_generator import ResponseGenerator
from .utils.helpers import load_config, validate_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Email:
    subject: str
    body: str
    sender: str
    received_date: datetime
    category: Optional[str] = None
    confidence: float = 0.0

class EmailProcessor:
    def __init__(self):
        self.config = load_config()
        self.classifier = EmailClassifier()
        self.response_generator = ResponseGenerator()
    
    def process_email(self, email_data: Dict) -> Dict:
        """Process a single email and generate an appropriate response."""
        try:
            # Validate email
            if not validate_email(email_data['sender']):
                raise ValueError(f"Invalid email address: {email_data['sender']}")
            
            # Create Email object
            email = Email(
                subject=email_data['subject'],
                body=email_data['body'],
                sender=email_data['sender'],
                received_date=datetime.now()
            )
            
            # Classify email
            category, confidence = self.classifier.classify(
                f"{email.subject} {email.body}"
            )
            email.category = category
            email.confidence = confidence
            
            # Generate response
            response = self.response_generator.generate_response(email)
            
            return {
                'success': True,
                'category': category,
                'confidence': confidence,
                'response': response,
                'email_id': id(email)
            }
            
        except Exception as e:
            logger.error(f"Error processing email: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 