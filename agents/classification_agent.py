from .base_agent import BaseAgent
from typing import Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class ClassificationAgent(BaseAgent):
    CATEGORIES = [
        "INQUIRY",
        "SUPPORT",
        "MEETING",
        "FOLLOW_UP"
    ]
    
    PRIORITY_LEVELS = ["LOW", "MEDIUM", "HIGH", "URGENT"]

    def __init__(self):
        super().__init__()
        self.model_name = "deepseek-ai/deepseek-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.CATEGORIES)
        )
        
        # Priority classification model
        self.priority_model = self._load_priority_model()

    async def process(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Combine subject and body for better context
            full_text = f"{email_data['subject']}\n\n{email_data['body']}"
            
            # Get category classification
            category_result = self._classify_category(full_text)
            
            # Get priority classification
            priority_result = self._classify_priority(full_text)
            
            # Determine next agent
            next_agent = self._determine_next_agent(category_result['category'])
            
            result = {
                'status': 'success',
                'classification': {
                    'category': category_result['category'],
                    'category_confidence': category_result['confidence'],
                    'priority': priority_result['priority'],
                    'priority_confidence': priority_result['confidence']
                },
                'next_agent': next_agent,
                'metadata': {
                    'message_id': email_data.get('message_id'),
                    'timestamp': email_data.get('timestamp')
                }
            }
            
            await self.log_processing(email_data, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Classification error: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    def _classify_category(self, text: str) -> Dict[str, Any]:
        """Classify email into categories"""
        inputs = self.tokenizer(
            text,
            truncation=True,
            padding=True,
            return_tensors="pt",
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            category_idx = torch.argmax(probabilities).item()
            confidence = probabilities[0][category_idx].item()
            
        return {
            'category': self.CATEGORIES[category_idx],
            'confidence': confidence,
            'all_probabilities': {
                cat: prob.item()
                for cat, prob in zip(self.CATEGORIES, probabilities[0])
            }
        }

    def _classify_priority(self, text: str) -> Dict[str, Any]:
        """Classify email priority"""
        # Use keywords and rules for priority classification
        keywords = {
            'URGENT': ['urgent', 'asap', 'emergency', 'immediate'],
            'HIGH': ['important', 'priority', 'critical'],
            'MEDIUM': ['please', 'when possible', 'need'],
            'LOW': ['fyi', 'update', 'newsletter']
        }
        
        text_lower = text.lower()
        scores = {level: 0.0 for level in self.PRIORITY_LEVELS}
        
        for level, words in keywords.items():
            for word in words:
                if word in text_lower:
                    scores[level] += 1
                    
        max_priority = max(scores.items(), key=lambda x: x[1])
        
        return {
            'priority': max_priority[0],
            'confidence': max_priority[1] / sum(scores.values()) if sum(scores.values()) > 0 else 0.5
        }

    def _determine_next_agent(self, category: str) -> str:
        """Determine which agent should handle the email next"""
        agent_mapping = {
            "INQUIRY": "InquiryResponderAgent",
            "SUPPORT": "SupportAgent",
            "MEETING": "MeetingResponderAgent",
            "FOLLOW_UP": "FollowUpAgent"
        }
        return agent_mapping.get(category, "InquiryResponderAgent")

    def _load_priority_model(self):
        """Load or initialize priority classification model"""
        # Implement priority model loading
        # This could be a separate ML model or rule-based system
        pass 