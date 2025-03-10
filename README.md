# Intelligent Multi-Agent Email Processing System

A sophisticated email automation system utilizing six specialized AI agents for comprehensive email processing and response generation.

## Table of Contents
- [System Overview](#system-overview)
- [Agent Architecture](#agent-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Development](#development)
- [Monitoring](#monitoring)

## System Overview

### Multi-Agent Architecture
```plaintext
                                ┌──────────────────┐
                                │   Email Input    │
                                └────────┬─────────┘
                                        │
                                        ▼
                                ┌──────────────────┐
                                │  Email Intake    │
                                │     Agent        │
                                └────────┬─────────┘
                                        │
                                        ▼
                                ┌──────────────────┐
                                │ Classification   │
                                │     Agent        │
                                └─┬──────┬──────┬──┘
                                  │      │      │
          ┌─────────────────┬────┴──┬───┴────┬─┴───────────┐
          ▼                 ▼        ▼        ▼             ▼
┌──────────────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ ┌─────────┐
│ Inquiry Response │ │ Support  │ │Meeting │ │Follow-up│ │  Other  │
│      Agent       │ │  Agent   │ │ Agent  │ │ Agent  │ │ Agents  │
└────────┬─────────┘ └────┬─────┘ └───┬────┘ └───┬────┘ └────┬────┘
         │                │           │          │           │
         └────────────────┴───────────┴──────────┴───────────┘
                                    │
                                    ▼
                            ┌──────────────────┐
                            │ Response Output  │
                            └──────────────────┘
```

## Agent Architecture

### 1. Email Intake Agent
Handles initial email processing and preparation.

```python
from agents.email_intake_agent import EmailIntakeAgent

intake_agent = EmailIntakeAgent()
result = await intake_agent.process(email_data)
```

**Features:**
- Email parsing and normalization
- Entity extraction
- Attachment handling
- Content cleaning
- Metadata extraction

**Configuration:**
```yaml
intake_agent:
  max_email_size: 10MB
  supported_attachments: ['pdf', 'doc', 'docx']
  entity_extraction: true
  content_cleaning: true
```

### 2. Classification Agent
Determines email category and routes to appropriate agent.

```python
from agents.classification_agent import ClassificationAgent

classifier = ClassificationAgent()
category = await classifier.process(parsed_email)
```

**Features:**
- Multi-category classification
- Priority determination
- Confidence scoring
- Intelligent routing

**Categories:**
- CLIENT_INQUIRY
- SUPPORT_REQUEST
- MEETING_REQUEST
- FOLLOW_UP

### 3. Inquiry Responder Agent
Handles general inquiries and information requests.

```python
from agents.inquiry_responder_agent import InquiryResponderAgent

inquiry_agent = InquiryResponderAgent()
response = await inquiry_agent.process(classified_email)
```

**Features:**
- Context-aware responses
- Template customization
- Professional formatting
- Brand voice maintenance

### 4. Support Agent
Processes technical support requests.

```python
from agents.support_agent import SupportAgent

support_agent = SupportAgent(knowledge_base_client)
response = await support_agent.process(support_request)
```

**Features:**
- Knowledge base integration
- Technical response generation
- Ticket creation
- Solution recommendation

### 5. Meeting Responder Agent
Handles meeting scheduling requests.

```python
from agents.meeting_responder_agent import MeetingResponderAgent

meeting_agent = MeetingResponderAgent(calendar_credentials)
response = await meeting_agent.process(meeting_request)
```

**Features:**
- Calendar availability checking
- Time slot suggestion
- Meeting scheduling
- Calendar event creation

### 6. Follow-up Agent
Manages follow-up communications.

```python
from agents.follow_up_agent import FollowUpAgent

follow_up_agent = FollowUpAgent(vector_db_client)
response = await follow_up_agent.process(follow_up_request)
```

**Features:**
- Conversation history analysis
- Personalized follow-ups
- Context maintenance
- Engagement tracking

## Implementation

### Base Agent Class
All agents inherit from the base agent class:

```python
class BaseAgent(ABC):
    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def log_processing(self, input_data: Dict[str, Any], 
                           result: Dict[str, Any]):
        pass
```

### Agent Orchestration
The EmailOrchestrator manages agent workflow:

```python
class EmailOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.intake_agent = EmailIntakeAgent()
        self.classification_agent = ClassificationAgent()
        self.inquiry_agent = InquiryResponderAgent()
        self.support_agent = SupportAgent(config['kb_client'])
        self.meeting_agent = MeetingResponderAgent(config['calendar'])
        self.follow_up_agent = FollowUpAgent(config['vector_db'])

    async def process_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation of email processing workflow
```

## Configuration

### Agent Configuration
Configure individual agents in `config/agents.yaml`:

```yaml
# Email Intake Agent
intake_agent:
  batch_size: 100
  supported_attachments: ['pdf', 'doc', 'docx', 'txt']
  max_content_length: 50000

# Classification Agent
classification_agent:
  model: deepseek-base
  confidence_threshold: 0.75
  categories:
    - INQUIRY
    - SUPPORT
    - MEETING
    - FOLLOW_UP

# Inquiry Agent
inquiry_agent:
  response_template_path: templates/inquiry
  max_response_length: 2000
  tone: professional

# Support Agent
support_agent:
  kb_index_path: kb/support
  ticket_system_url: http://support.example.com
  response_template_path: templates/support

# Meeting Agent
meeting_agent:
  calendar_id: primary
  meeting_duration_default: 60
  timezone: UTC
  max_suggestions: 5

# Follow-up Agent
follow_up_agent:
  history_lookup_days: 30
  vector_db_collection: conversations
  response_template_path: templates/follow_up
```

## Usage Examples

### 1. Processing a New Email

```python
from workflow.email_orchestrator import EmailOrchestrator

# Initialize orchestrator
orchestrator = EmailOrchestrator(config)

# Process email
email_data = {
    "sender": "user@example.com",
    "subject": "Meeting Request",
    "content": "Can we schedule a meeting...",
    "timestamp": "2024-01-20T10:00:00Z"
}

result = await orchestrator.process_email(email_data)
```

### 2. Using Individual Agents

```python
# Classification
classification_result = await classification_agent.process({
    "subject": "Technical Issue",
    "content": "I'm having problems with..."
})

# Support Response
support_response = await support_agent.process({
    "ticket_id": "T123",
    "category": "SUPPORT",
    "content": "Error message..."
})

# Meeting Scheduling
meeting_response = await meeting_agent.process({
    "sender": "client@example.com",
    "preferred_times": ["2024-01-21T14:00:00Z"]
})
```

## API Endpoints

### Email Processing
```bash
# Process new email
POST /api/v1/emails/process

# Get processing status
GET /api/v1/emails/{email_id}/status

# Get agent-specific response
GET /api/v1/emails/{email_id}/response/{agent_type}
```

### Agent Management
```bash
# Get agent status
GET /api/v1/agents/{agent_name}/status

# Update agent configuration
PUT /api/v1/agents/{agent_name}/config
```

## Monitoring

### Agent Metrics
- Processing time per agent
- Success/failure rates
- Classification accuracy
- Response quality scores

### System Metrics
- Queue sizes
- Response times
- Resource usage
- Error rates

### Dashboards
Access monitoring at:
- Metrics: `http://localhost:9090`
- Agent Logs: `http://localhost:5601`
- Traces: `http://localhost:16686`

## Development

### Adding a New Agent

1. Create new agent class:
```python
from agents.base_agent import BaseAgent

class NewAgent(BaseAgent):
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation
        pass
```

2. Register in orchestrator:
```python
self.agent_mapping["NEW_CATEGORY"] = NewAgent()
```

3. Add configuration:
```yaml
new_agent:
  setting1: value1
  setting2: value2
```

## Security

### Agent Security
- Input validation
- Output sanitization
- Rate limiting
- Access control

### Data Security
   - Email encryption
- Secure storage
   - PII handling
   - Audit logging

## Testing

### Agent Testing
```python
# Test classification
python -m pytest tests/agents/test_classification_agent.py

# Test response generation
python -m pytest tests/agents/test_response_agents.py
```

### Integration Testing
```python
# Test full workflow
python -m pytest tests/integration/test_workflow.py
```

## Contributing

1. Fork repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.