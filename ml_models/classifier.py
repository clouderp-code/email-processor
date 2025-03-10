from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class EmailClassifier:
    def __init__(self):
        self.model_name = "bert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
    def classify(self, email_content):
        inputs = self.tokenizer(email_content, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=1)
        return {
            "category": self.model.config.id2label[predictions.argmax().item()],
            "confidence": predictions.max().item()
        } 