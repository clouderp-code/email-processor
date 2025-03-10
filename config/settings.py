from pydantic import BaseSettings

class Settings(BaseSettings):
    # ... existing settings ...
    
    # AI Model Settings
    CLASSIFIER_MODEL_PATH: str = "models/classifier"
    RESPONSE_MODEL_NAME: str = "deepseek-r1"
    MIN_CONFIDENCE_THRESHOLD: float = 0.75
    
    # Email Processing
    AUTO_SEND_THRESHOLD: float = 0.95  # Auto-send if confidence > 95%
    MAX_RESPONSE_LENGTH: int = 2000
    ENABLE_AUTO_FOLLOW_UP: bool = True
    
    # Knowledge Base
    KB_INDEX_PATH: str = "data/kb_index"
    KB_UPDATE_INTERVAL: int = 3600  # 1 hour 