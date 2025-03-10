# Enhanced Email Processor with Gmail Integration

A sophisticated email processing system that combines ML-powered classification, automated response generation, and Gmail integration for real-time email processing.

## Table of Contents
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Gmail Integration Setup](#gmail-integration-setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Monitoring & Analytics](#monitoring--analytics)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## Features

### Core Features
- 🤖 ML-powered email classification and response generation
- 📧 Real-time Gmail integration and monitoring
- 🔐 Authentication and authorization
- 📊 Comprehensive monitoring and analytics
- 🚀 RESTful API endpoints
- 💾 Database integration for email storage
- 📝 Detailed logging system

### Gmail Integration Features
- Real-time email monitoring
- Automatic email processing
- Manual sync capabilities
- Multi-part email handling
- Secure OAuth2 authentication
- Configurable sync intervals

## System Architecture

```plaintext
┌─────────────────┐     ┌──────────────────┐     ┌────────────────┐
│  Gmail Service  │────▶│  Async Worker    │────▶│  ML Processor  │
└─────────────────┘     └──────────────────┘     └────────────────┘
         │                       │                        │
         │                       │                        │
         ▼                       ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Database Layer                         │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Google Cloud Platform account
- Gmail account with API access
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/enhanced-email-processor.git
cd enhanced-email-processor
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### 1. Environment Variables
Create `.env` file in project root:
```env
# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/email_processor
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Authentication
SECRET_KEY=your-secure-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gmail Configuration
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.pickle
GMAIL_SYNC_INTERVAL=60

# ML Model Settings
MODEL_PATH=models/classifier
MODEL_VERSION=1.0
CONFIDENCE_THRESHOLD=0.75

# Monitoring
ENABLE_PROMETHEUS=true
METRICS_PORT=9090
LOG_LEVEL=INFO
```

### 2. Database Setup
```bash
# Create database
createdb email_processor

# Run migrations
python database/migrations.py
```

## Gmail Integration Setup

### 1. Google Cloud Platform Setup

1. Create new project in [Google Cloud Console](https://console.cloud.google.com)
2. Enable Gmail API:
   ```
   Dashboard → Enable APIs and Services → Gmail API → Enable
   ```

3. Configure OAuth Consent Screen:
   - Go to "OAuth consent screen"
   - Choose "External"
   - Fill in application details
   - Add required scopes:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.modify`

4. Create OAuth Credentials:
   - Go to "Credentials"
   - Create "OAuth 2.0 Client ID"
   - Application type: Desktop Application
   - Download JSON and save as `credentials.json`

### 2. Application Configuration

1. Place credentials:
```bash
mv credentials.json /path/to/project/credentials.json
```

2. First-time authentication:
```bash
python scripts/gmail_auth.py
```

### 3. Gmail Monitoring Configuration

Configure monitoring parameters in `.env`:
```env
GMAIL_SYNC_INTERVAL=60  # Check interval in seconds
GMAIL_BATCH_SIZE=100    # Number of emails per batch
GMAIL_ERROR_RETRY=300   # Retry interval on error (seconds)
```

## Usage

### Starting the Server

1. Start the application:
```bash
uvicorn main:app --reload
```

2. Access the application:
- API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`

### API Documentation

#### Authentication Endpoints

```bash
POST /auth/register
{
    "username": "user@example.com",
    "password": "secure_password"
}

POST /auth/login
{
    "username": "user@example.com",
    "password": "secure_password"
}
```

#### Email Processing Endpoints

```bash
# Process single email
POST /api/v1/emails/process
{
    "sender": "sender@example.com",
    "subject": "Test Subject",
    "content": "Email content here"
}

# Get processed emails
GET /api/v1/emails?page=1&limit=10

# Get specific email
GET /api/v1/emails/{email_id}
```

#### Gmail Integration Endpoints

```bash
# Manual sync
POST /api/v1/gmail/sync

# Get Gmail status
GET /api/v1/gmail/status

# Configure Gmail settings
PUT /api/v1/gmail/config
{
    "sync_interval": 60,
    "batch_size": 100
}
```

## Monitoring & Analytics

### Available Metrics

1. Email Processing Metrics:
   - Total emails processed
   - Processing time distribution
   - Success/failure rates
   - ML model confidence scores

2. Gmail Specific Metrics:
   - Sync operations
   - New emails detected
   - Processing queue size
   - Error rates

### Accessing Metrics

1. Prometheus Endpoint:
```bash
GET /metrics
```

2. Grafana Dashboard:
   - Import provided dashboard template
   - Configure data source
   - Access at `http://localhost:3000`

## Development Guide

### Project Structure
```
project/
├── api/               # API endpoints and authentication
├── config/            # Configuration settings
├── database/          # Database models and connection
├── ml_models/         # ML model implementations
├── monitoring/        # Metrics and logging
├── requirements.txt   # Project dependencies
└── main.py           # Application entry point
```

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. Database Connection Issues
```bash
# Check database status
sudo service postgresql status

# Verify database URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/email_processor
```

2. ML Model Loading Issues
```bash
# Ensure model files are downloaded
python -m ml_models.download_models
```

### Getting Help

- Open an issue in the GitHub repository
- Check the logs in `logs/app.log`
- Consult the API documentation at `/docs`

## Performance Optimization

For production deployment, consider:
- Using Gunicorn as a WSGI server
- Implementing caching (Redis recommended)
- Setting up database indexing
- Configuring proper logging levels

## Security Considerations

- Keep your `.env` file secure and never commit it
- Regularly update dependencies
- Use strong passwords for database and JWT secrets
- Implement rate limiting for API endpoints
- Regular security audits

## Acknowledgments

- FastAPI for the excellent web framework
- Transformers library for ML capabilities
- SQLAlchemy for database operations

### Adding New Features

1. Adding a New Email Category:
```python
# 1. Update CATEGORIES in classifier_agent.py
CATEGORIES = [..., "NEW_CATEGORY"]

# 2. Create new responder in response_generators.py
class NewCategoryResponder(BaseResponseGenerator):
    async def generate_response(self, email_data):
        # Implementation
```

## Troubleshooting

### Common Issues

1. Classification Issues:
```bash
# Retrain classifier
python scripts/train_classifier.py --data-path data/training

# Test classification
python scripts/test_classifier.py --email-file test.eml
```

2. Response Generation Issues:
```bash
# Test response generation
python scripts/test_response.py --category MEETING_REQUEST

# Update knowledge base
python scripts/update_kb.py
```

## Security Considerations

1. Email Content Security:
   - Content encryption
   - PII detection and handling
   - Secure storage practices

2. API Security:
   - Rate limiting
   - Request validation
   - Authentication checks

3. Model Security:
   - Input sanitization
   - Output validation
   - Model version control

## Performance Optimization

1. Processing Optimization:
   - Batch processing
   - Caching strategies
   - Async processing

2. Response Generation:
   - Template caching
   - Knowledge base indexing
   - Response quality checks

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Adding New Agents

1. Create new agent class:
```python
from agents.base_agent import BaseAgent

class NewAgent(BaseAgent):
    async def process(self, data):
        # Implementation
        pass
```

2. Register in orchestrator:
```python
self.agent_mapping["NEW_CATEGORY"] = NewAgent()
```

## Monitoring

### Available Metrics

1. Agent Performance:
   - Processing time
   - Success rates
   - Error rates
   - Classification accuracy

2. System Metrics:
   - Queue sizes
   - Response times
   - Resource usage

3. Business Metrics:
   - Email categories distribution
   - Response satisfaction
   - Processing volume

### Dashboards

Access monitoring at:
- Metrics: `http://localhost:9090`
- Logs: `http://localhost:5601`
- Traces: `http://localhost:16686`

## Troubleshooting

### Common Issues

1. Agent Failures:
```bash
# Check agent logs
tail -f logs/agents.log

# Reset agent state
python scripts/reset_agent.py --agent classification
```

2. Integration Issues:
```bash
# Test Gmail connection
python scripts/test_gmail.py

# Verify calendar access
python scripts/test_calendar.py
```

3. Performance Issues:
```bash
# Check queue status
python scripts/check_queues.py

# Monitor processing times
python scripts/monitor_performance.py
```

## Security

1. Data Protection:
   - Email encryption
   - Secure credential storage
   - PII handling

2. Access Control:
   - API authentication
   - Agent permissions
   - Audit logging

## Contributing

1. Fork repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.