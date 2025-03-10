from fastapi import APIRouter, Depends, HTTPException
from typing import List
from database.models import Email, Response
from api.auth import get_current_user
from monitoring.metrics import track_request
from ml_models.classifier import EmailClassifier

router = APIRouter()
classifier = EmailClassifier()

@router.post("/emails/process")
async def process_email(
    email_data: dict,
    current_user = Depends(get_current_user)
):
    try:
        # Track request
        track_request("process_email")
        
        # Process email
        classification = classifier.classify(email_data["content"])
        
        # Store in database
        email = Email(
            sender=email_data["sender"],
            subject=email_data["subject"],
            content=email_data["content"],
            category=classification["category"],
            confidence=classification["confidence"],
            user_id=current_user.id
        )
        
        # Generate and store response
        response = Response(
            email=email,
            content=generate_response(email_data, classification),
            model_version="1.0"
        )
        
        return {
            "success": True,
            "classification": classification,
            "response": response.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 