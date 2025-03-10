from typing import Tuple
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from ..utils.helpers import load_config

class EmailClassifier:
    def __init__(self):
        config = load_config()
        self.vectorizer = TfidfVectorizer(
            max_features=config['model_settings']['max_features']
        )
        self.classifier = MultinomialNB()
        self.categories = None
        
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
    
    def train(self, texts, labels):
        """Train the classifier with example data."""
        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)
        self.categories = list(set(labels))
    
    def classify(self, text: str) -> Tuple[str, float]:
        """Classify an email text and return the category and confidence."""
        if self.categories is None:
            return 'general', 0.0
        
        X = self.vectorizer.transform([text])
        category = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        confidence = np.max(probabilities)
        
        return category, float(confidence) 