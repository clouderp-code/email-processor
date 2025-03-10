from jinja2 import Template
from ..utils.helpers import load_config

class ResponseGenerator:
    def __init__(self):
        self.config = load_config()
        self.templates = self.config['response_templates']
    
    def generate_response(self, email) -> str:
        """Generate a response based on the email category and content."""
        category = email.category or 'general'
        template_data = self.templates.get(category, self.templates['general'])
        
        response_template = """
{{ greeting }}

We have received your email regarding: "{{ subject }}"

{{ custom_message }}

{{ closing }}
"""
        
        custom_message = self._generate_custom_message(email)
        
        template = Template(response_template)
        return template.render(
            greeting=template_data['greeting'],
            subject=email.subject,
            custom_message=custom_message,
            closing=template_data['closing']
        )
    
    def _generate_custom_message(self, email) -> str:
        """Generate a custom message based on the email category."""
        messages = {
            'support': "Our support team will review your request and get back to you within 24 hours.",
            'billing': "Our billing team will review your inquiry and respond as soon as possible.",
            'sales': "A sales representative will contact you shortly with detailed information.",
            'technical': "Our technical team will analyze your issue and provide a solution soon.",
            'general': "We will review your message and respond appropriately."
        }
        return messages.get(email.category, messages['general']) 