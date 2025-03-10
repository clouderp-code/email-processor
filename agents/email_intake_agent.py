from .base_agent import BaseAgent
from typing import Dict, Any
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

class EmailIntakeAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.email_patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        }

    async def process(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming email and extract relevant information"""
        try:
            # Parse email content
            parsed_email = self._parse_email(email_data)
            
            # Extract entities
            entities = self._extract_entities(parsed_email['body'])
            
            # Clean and normalize content
            cleaned_content = self._clean_content(parsed_email['body'])
            
            result = {
                'status': 'success',
                'message_id': email_data.get('message_id'),
                'parsed_data': {
                    'sender': parsed_email['sender'],
                    'subject': parsed_email['subject'],
                    'body': cleaned_content,
                    'recipients': parsed_email['recipients'],
                    'timestamp': parsed_email['timestamp'],
                    'entities': entities,
                    'attachments': parsed_email['attachments']
                }
            }
            
            await self.log_processing(email_data, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing email: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    def _parse_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse raw email data into structured format"""
        msg = email.message_from_string(email_data['raw_content'])
        
        return {
            'sender': msg['from'],
            'subject': msg['subject'],
            'body': self._get_email_body(msg),
            'recipients': msg['to'],
            'timestamp': msg['date'],
            'attachments': self._get_attachments(msg)
        }

    def _extract_entities(self, content: str) -> Dict[str, list]:
        """Extract relevant entities from email content"""
        entities = {}
        for entity_type, pattern in self.email_patterns.items():
            entities[entity_type] = re.findall(pattern, content)
        return entities

    def _clean_content(self, content: str) -> str:
        """Clean and normalize email content"""
        # Remove email signatures
        content = re.split(r'-{2,}|_{2,}', content)[0]
        
        # Remove extra whitespace
        content = ' '.join(content.split())
        
        # Remove quoted replies
        content = re.sub(r'On.*wrote:|>.*', '', content)
        
        return content.strip()

    def _get_email_body(self, msg) -> str:
        """Extract email body from message"""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return msg.get_payload(decode=True).decode()

    def _get_attachments(self, msg) -> list:
        """Extract attachments from email"""
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                
                filename = part.get_filename()
                if filename:
                    attachments.append({
                        'filename': filename,
                        'content_type': part.get_content_type(),
                        'size': len(part.get_payload())
                    })
        return attachments 