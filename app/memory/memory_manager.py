from utils.timezone_utils import now_central
"""
Unified Memory Manager orchestrating all four memory layers
Provides a single interface for context-aware, personalized responses
"""

from typing import Dict, List, Optional
from datetime import datetime

from app.memory.short_term_memory import ShortTermMemory
from app.memory.long_term_memory import LongTermMemory
from app.memory.episodic_memory import EpisodicMemory
from app.memory.structured_memory import StructuredMemory


class MemoryManager:
    """Unified interface for all memory layers"""
    
    def __init__(self):
        """Initialize all memory layers"""
        self.short_term = ShortTermMemory(max_size=15)
        self.long_term = LongTermMemory()
        self.episodic = EpisodicMemory()
        self.structured = StructuredMemory()
    
    def add_conversation(self, user_id: int, user_message: str, 
                        assistant_response: str, timestamp: datetime = None):
        """
        Add a conversation to memory system
        
        Args:
            user_id: User ID
            user_message: User's message
            assistant_response: Assistant's response
            timestamp: Timestamp of conversation
        """
        # Add to short-term memory
        self.short_term.add_exchange(user_message, assistant_response, timestamp)
        
        # Long-term memory will update automatically when queried
        # (rebuilds index periodically)
    
    def get_full_context(self, user_id: int, current_query: str) -> str:
        """
        Get comprehensive context from all memory layers
        
        Args:
            user_id: User ID
            current_query: Current user query
        
        Returns:
            Complete context string for AI prompt
        """
        context_parts = []
        
        # 1. Structured Memory - User Profile and Preferences
        profile = self.structured.get_formatted_profile(user_id)
        if profile:
            context_parts.append("=== USER PROFILE ===")
            context_parts.append(profile)
        
        # 2. Short-Term Memory - Recent conversation
        short_term_context = self.short_term.get_formatted_context(num_exchanges=5)
        if short_term_context and "No recent" not in short_term_context:
            context_parts.append("\n=== RECENT CONVERSATION ===")
            context_parts.append(short_term_context)
        
        # 3. Long-Term Memory - Semantically similar past conversations
        similar_context = self.long_term.get_formatted_similar_context(
            current_query, user_id, top_k=2
        )
        if similar_context:
            context_parts.append("\n=== RELEVANT PAST CONVERSATIONS ===")
            context_parts.append(similar_context)
        
        # 4. Episodic Memory - Recent daily summaries
        recent_summaries = self.episodic.get_recent_summaries(user_id, days=3)
        if recent_summaries:
            context_parts.append("\n=== RECENT DAILY SUMMARIES ===")
            for summary in recent_summaries[:2]:  # Only include last 2 days
                summary_text = self.episodic.get_formatted_summary(
                    user_id, summary.date
                )
                context_parts.append(summary_text)
        
        return "\n".join(context_parts)
    
    def recall_information(self, user_id: int, query: str) -> str:
        """
        Intelligently recall specific information based on query
        
        Args:
            user_id: User ID
            query: User's query
        
        Returns:
            Relevant information
        """
        query_lower = query.lower()
        
        # Check for specific query types
        if any(word in query_lower for word in ['medication', 'medicine', 'pill', 'schedule']):
            return self.structured.get_medication_schedule(user_id)
        
        elif any(word in query_lower for word in ['breakfast', 'lunch', 'dinner', 'meal', 'eat']):
            logs = self.structured.get_daily_logs(user_id)
            if logs["meals"]:
                return f"Today you mentioned: {', '.join(logs['meals'])}"
            else:
                # Search in past conversations
                similar = self.long_term.retrieve_similar_conversations(query, user_id, top_k=3)
                if similar:
                    for conv in similar:
                        if any(meal in conv['user_message'].lower() for meal in ['breakfast', 'lunch', 'dinner']):
                            return f"I remember you mentioned: {conv['user_message']}"
                return "I don't have a specific record. Can you tell me more?"
        
        elif any(word in query_lower for word in ['remember', 'talked about', 'discussed', 'said']):
            # Recall from long-term memory
            similar = self.long_term.retrieve_similar_conversations(query, user_id, top_k=3)
            if similar:
                response = "Yes, I remember we talked about:\n"
                for conv in similar[:2]:
                    date_str = conv['timestamp'].strftime('%B %d')
                    response += f"\n[{date_str}] You: {conv['user_message'][:100]}...\n"
                return response
            else:
                return "I'm not finding a specific memory of that. Could you give me more details?"
        
        elif any(word in query_lower for word in ['today', 'yesterday', 'summary']):
            # Get episodic summary
            date = now_central()
            if 'yesterday' in query_lower:
                from datetime import timedelta
                date = date - timedelta(days=1)
            
            summary = self.episodic.get_formatted_summary(user_id, date)
            return summary
        
        else:
            # General recall from structured memory
            return self.structured.recall_specific_info(user_id, query)
    
    def generate_daily_summary(self, user_id: int):
        """
        Generate daily summary for episodic memory
        
        Args:
            user_id: User ID
        """
        return self.episodic.generate_daily_summary(user_id)
    
    def update_long_term_index(self, user_id: int):
        """
        Update long-term memory index
        
        Args:
            user_id: User ID
        """
        self.long_term.build_memory_index(user_id)
    
    def clear_short_term(self):
        """Clear short-term memory buffer"""
        self.short_term.clear()
    
    def get_memory_stats(self, user_id: int) -> Dict:
        """
        Get statistics about memory system
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with memory stats
        """
        return {
            "short_term_size": self.short_term.get_size(),
            "long_term_conversations": len(self.long_term.conversation_ids),
            "recent_summaries": len(self.episodic.get_recent_summaries(user_id, days=7)),
            "medications_count": len(self.structured.get_medication_schedule(user_id).split('\n')) - 2
        }
