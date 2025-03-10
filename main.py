from fastapi import FastAPI
from database.database import init_db
from api.routes import router
from api.auth import auth_router
from monitoring.metrics import init_metrics
import logging
from workflow.email_orchestrator import EmailOrchestrator
from agents.gmail_async_worker import GmailAsyncWorker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Enhanced Email Processor")

# Initialize components
def init_application():
    # Initialize database
    init_db()
    
    # Initialize monitoring
    init_metrics()
    
    # Register routers
    app.include_router(router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/auth")
    
    # Initialize email orchestrator
    global email_orchestrator
    email_orchestrator = EmailOrchestrator(gmail_service, database)
    
    # Update Gmail worker to use orchestrator
    global async_worker
    async_worker = GmailAsyncWorker(gmail_service, email_orchestrator)

# Startup event
@app.on_event("startup")
async def startup_event():
    init_application()

# Add new endpoints for managing email processing
@app.get("/api/v1/emails/drafts")
async def get_email_drafts():
    """Get all draft responses"""
    drafts = await gmail_service.list_drafts()
    return {"drafts": drafts}

@app.post("/api/v1/emails/drafts/{draft_id}/send")
async def send_draft(draft_id: str):
    """Send a draft email"""
    try:
        await gmail_service.send_draft(draft_id)
        return {"status": "success", "message": "Draft sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)