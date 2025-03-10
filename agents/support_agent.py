from .base_agent import BaseAgent
from typing import Dict, Any
import openai
from datetime import datetime

class SupportAgent(BaseAgent):
    def __init__(self, knowledge_base_client):
        super().__init__()
        self.kb_client = knowledge_base_client
        self.templates = self._load_templates()

    async def process(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Search knowledge base
            kb_results = await self._search_knowledge_base(email_data['body'])
            
            # Generate support response
            response_content = await self._generate_support_response(
                email_data,
                kb_results
            )
            
            # Format response
            formatted_response = self._format_response(
                response_content,
                email_data
            )
            
            # Create support ticket
            ticket_id = await self._create_support_ticket(
                email_data,
                response_content
            )
            
            result = {
                'status': 'success',
                'response': {
                    'content': formatted_response,
                    'ticket_id': ticket_id,
                    'kb_articles': kb_results['articles'],
                    'type': 'SUPPORT_RESPONSE',
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            await self.log_processing(email_data, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating support response: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    async def _search_knowledge_base(self, query: str) -> Dict[str, Any]:
        """Search knowledge base for relevant articles"""
        try:
            results = await self.kb_client.search(
                query=query,
                limit=3,
                min_relevance=0.7
            )
            
            return {
                'articles': results,
                'total_found': len(results)
            }
        except Exception as e:
            self.logger.error(f"Knowledge base search error: {str(e)}")
            return {'articles': [], 'total_found': 0}

    async def _generate_support_response(
        self,
        email_data: Dict[str, Any],
        kb_results: Dict[str, Any]
    ) -> str:
        """Generate support response using AI and KB articles"""
        prompt = self._create_support_prompt(email_data, kb_results)
        
        response = await openai.Completion.create(
            model="deepseek-r1",
            prompt=prompt,
            max_tokens=800,
            temperature=0.5
        )
        
        return response.choices[0].text.strip()

    async def _create_support_ticket(
        self,
        email_data: Dict[str, Any],
        response: str
    ) -> str:
        """Create support ticket in ticketing system"""
        ticket_data = {
            'subject': email_data['subject'],
            'description': email_data['body'],
            'response': response,
            'customer_email': email_data['sender'],
            'priority': email_data.get('priority', 'MEDIUM'),
            'status': 'OPEN'
        }
        
        # Implement ticket creation logic
        ticket_id = "TICKET-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        return ticket_id

    def _create_support_prompt(
        self,
        email_data: Dict[str, Any],
        kb_results: Dict[str, Any]
    ) -> str:
        """Create prompt for support response generation"""
        kb_content = "\n".join([
            f"Article {i+1}: {article['content']}"
            for i, article in enumerate(kb_results['articles'])
        ])
        
        return f"""
        Generate a technical support response:
        
        Customer Issue:
        {email_data['body']}
        
        Relevant Knowledge Base Articles:
        {kb_content}
        
        Requirements:
        - Provide clear step-by-step solutions
        - Reference relevant documentation
        - Include troubleshooting steps
        - Maintain professional tone
        - Include ticket reference number
        
        Response:
        """ 