from .base_agent import BaseAgent
from typing import Dict, Any
import openai
from datetime import datetime

class FollowUpAgent(BaseAgent):
    def __init__(self, vector_db_client):
        super().__init__()
        self.vector_db = vector_db_client
        self.templates = self._load_templates()

    async def process(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Get conversation history
            history = await self._get_conversation_history(email_data['sender'])
            
            # Generate follow-up response
            response_content = await self._generate_follow_up(
                email_data,
                history
            )
            
            # Format response
            formatted_response = self._format_response(
                response_content,
                email_data,
                history
            )
            
            result = {
                'status': 'success',
                'response': {
                    'content': formatted_response,
                    'type': 'FOLLOW_UP',
                    'conversation_id': history.get('conversation_id'),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            await self.log_processing(email_data, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating follow-up: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    async def _get_conversation_history(self, sender: str) -> Dict[str, Any]:
        """Retrieve conversation history from vector database"""
        try:
            history = await self.vector_db.search(
                query=f"sender:{sender}",
                limit=5,
                sort_by="timestamp",
                sort_order="desc"
            )
            
            return {
                'conversation_id': history.get('conversation_id'),
                'messages': history.get('messages', []),
                'last_interaction': history.get('last_interaction')
            }
        except Exception as e:
            self.logger.error(f"Error retrieving conversation history: {str(e)}")
            return {'messages': []}

    async def _generate_follow_up(
        self,
        email_data: Dict[str, Any],
        history: Dict[str, Any]
    ) -> str:
        """Generate personalized follow-up response"""
        prompt = self._create_follow_up_prompt(email_data, history)
        
        response = await openai.Completion.create(
            model="deepseek-r1",
            prompt=prompt,
            max_tokens=600,
            temperature=0.7
        )
        
        return response.choices[0].text.strip()

    def _create_follow_up_prompt(
        self,
        email_data: Dict[str, Any],
        history: Dict[str, Any]
    ) -> str:
        """Create prompt for follow-up generation"""
        conversation_context = "\n".join([
            f"Message {i+1}: {msg['content']}"
            for i, msg in enumerate(history['messages'])
        ])
        
        return f"""
        Generate a personalized follow-up email response:
        
        Original Email:
        {email_data['body']}
        
        Conversation History:
        {conversation_context}
        
        Requirements:
        - Reference previous interactions
        - Maintain conversation context
        - Be proactive about next steps
        - Keep tone consistent with previous interactions
        - Address any outstanding items
        
        Response:
        """

    def _format_response(
        self,
        content: str,
        email_data: Dict[str, Any],
        history: Dict[str, Any]
    ) -> str:
        """Format the follow-up response"""
        template = self.templates['follow_up']
        
        return template.format(
            recipient_name=self._extract_name(email_data['sender']),
            content=content,
            previous_reference=self._get_previous_reference(history),
            signature=self._get_signature()
        )

    def _get_previous_reference(self, history: Dict[str, Any]) -> str:
        """Get reference to previous conversation"""
        if not history['messages']:
            return ""
            
        last_interaction = history['messages'][0]
        return f"Regarding our previous conversation on {last_interaction['timestamp']}"

    def _load_templates(self) -> Dict[str, str]:
        """Load email templates"""
        return {
            'follow_up': """
            Dear {recipient_name},

            {previous_reference}

            {content}

            {signature}
            """
        } 