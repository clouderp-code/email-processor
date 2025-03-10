import yaml
from pathlib import Path
from email_validator import validate_email as validate_email_address, EmailNotValidError

def load_config():
    """Load configuration from YAML file."""
    config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def validate_email(email: str) -> bool:
    """Validate email address format."""
    try:
        validate_email_address(email)
        return True
    except EmailNotValidError:
        return False 