from typing import Dict, Any
from agents.email_intake_agent import EmailIntakeAgent
from agents.classification_agent import ClassificationAgent
from agents.inquiry_responder_agent import InquiryResponderAgent
from agents.support_agent import SupportAgent
from agents.meeting_responder_agent import MeetingResponderAgent
from agents.follow_up_agent import FollowUpAgent

class EmailOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.intake_agent = EmailIntakeAgent()
        self.classification_agent = ClassificationAgent()
        self.inquiry_agent = InquiryResponderAgent()
        self.support_agent = SupportAgent(config['knowledge_base_client'])
        self.meeting_agent = MeetingResponderAgent(config['calendar_credentials'])
        self.follow_up_agent = FollowUpAgent(config['vector_db_client'])
        
        self.agent_mapping = {
            "INQUIRY": self.inquiry_agent,
            "SUPPORT": self.support_agent,
            "MEETING": self.meeting_agent,
            "FOLLOW_UP": self.follow_up_agent
        }

    async def process_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 1. Process incoming email
            intake_result = await self.intake_agent.process(email_data)
            if intake_result['status'] != 'success':
                return intake_result
                
            # 2. Classify email
            classification_result = await self.classification_agent.process(
                intake_result['parsed_data']
            )
            if classification_result['status'] != 'success':
                return classification_result
                
            # 3. Route to appropriate agent
            category = classification_result['classification']['category']
            agent = self.agent_mapping.get(category)
            
            if not agent:
                return {
                    'status': 'error',
                    'error': f"No agent found for category: {category}"
                }
                
            # 4. Process with specific agent
            result = await agent.process({
                **intake_result['parsed_data'],
                **classification_result['classification']
            })
            
            return result
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)} 