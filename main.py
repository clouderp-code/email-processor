from fastapi import FastAPI
from database.database import init_db
from api.routes import router
from api.auth import auth_router
from monitoring.metrics import init_metrics
import logging

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

# Startup event
@app.on_event("startup")
async def startup_event():
    init_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)