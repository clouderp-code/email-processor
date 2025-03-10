from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return results"""
        pass
    
    async def log_processing(self, input_data: Dict[str, Any], result: Dict[str, Any]):
        """Log processing details"""
        self.logger.info(
            f"Processing completed - Input: {input_data.get('id', 'N/A')} "
            f"Result: {result.get('status', 'unknown')}"
        ) 