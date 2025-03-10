from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Any
import numpy as np

class EmailClassifier:
    CATEGORIES = [
        "CLIENT_INQUIRY",
        "SUPPORT_REQUEST",
        "INTRODUCTION_EMAIL",
        "MEETING_REQUEST",
        "FOLLOW_UP"
    ]

    def __init__(self):
        self.model_name = "deepseek-ai/deepseek-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.CATEGORIES)
        )
        
    def classify_email(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classifies an email based on its content and metadata
        """
        # Combine subject and content for better context
        full_text = f"{email_content['subject']}\n\n{email_content['content']}"
        
        # Tokenize and predict
        inputs = self.tokenizer(
            full_text,
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
            "category": self.CATEGORIES[category_idx],
            "confidence": confidence,
            "all_probabilities": {
                cat: prob.item()
                for cat, prob in zip(self.CATEGORIES, probabilities[0])
            }
        } 