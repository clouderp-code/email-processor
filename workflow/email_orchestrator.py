from typing import Dict, Any
import asyncio
from agents.classifier_agent import EmailClassifier
from agents.response_generators import (
    ClientInquiryResponder,
    SupportRequestResponder,
    MeetingResponder,
    FollowUpResponder
)
from monitoring.metrics import track_processing_time
from database.models import Email, Response
import logging

logger = logging.getLogger(__name__)

class EmailOrchestrator:
    def __init__(self, gmail_service, database):
        self.gmail_service = gmail_service
        self.database = database
        self.classifier = EmailClassifier()
        
        # Initialize responders
        self.responders = {
            "CLIENT_INQUIRY": ClientInquiryResponder(),
            "SUPPORT_REQUEST": SupportRequestResponder(),
            "MEETING_REQUEST": MeetingResponder(gmail_service.credentials),
            "FOLLOW_UP": FollowUpResponder(database.vector_db)
        }
        
    @track_processing_time
    async def process_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main workflow for processing an email
        """
        try:
            # 1. Classify email
            classification = self.classifier.classify_email(email_data)
            
            # 2. Log classification
            logger.info(f"Email classified as {classification['category']} "
                       f"with confidence {classification['confidence']:.2f}")
            
            # 3. Generate response
            responder = self.responders.get(classification['category'])
            if not responder:
                raise ValueError(f"No responder for category: {classification['category']}")
            
            response_text = await responder.generate_response(email_data)
            
            # 4. Create Gmail draft
            draft_id = await self.create_gmail_draft(
                email_data['message_id'],
                response_text
            )
            
            # 5. Store in database
            await self.store_processed_email(
                email_data,
                classification,
                response_text,
                draft_id
            )
            
            return {
                "success": True,
                "category": classification['category'],
                "confidence": classification['confidence'],
                "draft_id": draft_id
            }
            
        except Exception as e:
            logger.error(f"Error processing email: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def create_gmail_draft(self, original_message_id: str, response_text: str) -> str:
        """Creates a draft response in Gmail"""
        try:
            draft = self.gmail_service.users().drafts().create(
                userId='me',
                body={
                    'message': {
                        'raw': response_text,
                        'threadId': original_message_id
                    }
                }
            ).execute()
            return draft['id']
        except Exception as e:
            logger.error(f"Error creating draft: {str(e)}")
            raise
    
    async def store_processed_email(
        self,
        email_data: Dict[str, Any],
        classification: Dict[str, Any],
        response_text: str,
        draft_id: str
    ):
        """Stores processed email and response in database"""
        async with self.database.session() as session:
            email = Email(
                message_id=email_data['message_id'],
                sender=email_data['sender'],
                subject=email_data['subject'],
                content=email_data['content'],
                category=classification['category'],
                confidence=classification['confidence']
            )
            session.add(email)
            
            response = Response(
                email=email,
                content=response_text,
                draft_id=draft_id,
                model_version="deepseek-r1"
            )
            session.add(response)
            await session.commit() 