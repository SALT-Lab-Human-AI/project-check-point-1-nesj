from utils.timezone_utils import now_central
"""
Short-term memory buffer for immediate conversation context
Uses in-memory deque to retain last 10-15 exchanges
"""

from collections import deque
from typing import List, Dict
from datetime import datetime


class ShortTermMemory:
    """Manages short-term conversation buffer"""
    
    def __init__(self, max_size: int = 15):
        """
        Initialize short-term memory buffer
        
        Args:
            max_size: Maximum number of exchanges to retain (default: 15)
        """
        self.buffer = deque(maxlen=max_size)
        self.max_size = max_size
    
    def add_exchange(self, user_message: str, assistant_response: str, 
                    timestamp: datetime = None):
        """Add a conversation exchange to the buffer"""
        if timestamp is None:
            timestamp = now_central()
        
        exchange = {
            "user_message": user_message,
            "assistant_response": assistant_response,
            "timestamp": timestamp
        }
        self.buffer.append(exchange)
    
    def get_recent_context(self, num_exchanges: int = None) -> List[Dict]:
        """
        Get recent conversation exchanges
        
        Args:
            num_exchanges: Number of recent exchanges to retrieve (default: all)
        
        Returns:
            List of conversation exchanges
        """
        if num_exchanges is None or num_exchanges >= len(self.buffer):
            return list(self.buffer)
        
        return list(self.buffer)[-num_exchanges:]
    
    def get_formatted_context(self, num_exchanges: int = None) -> str:
        """
        Get formatted string of recent context for AI prompts
        
        Args:
            num_exchanges: Number of recent exchanges to include
        
        Returns:
            Formatted conversation context
        """
        exchanges = self.get_recent_context(num_exchanges)
        
        if not exchanges:
            return "No recent conversation history."
        
        context = "Recent conversation context:\n"
        for exchange in exchanges:
            context += f"User: {exchange['user_message']}\n"
            context += f"Carely: {exchange['assistant_response']}\n"
            context += "---\n"
        
        return context
    
    def clear(self):
        """Clear the short-term memory buffer"""
        self.buffer.clear()
    
    def get_size(self) -> int:
        """Get current number of exchanges in buffer"""
        return len(self.buffer)
