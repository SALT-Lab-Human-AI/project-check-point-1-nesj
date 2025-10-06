from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
from app.database.crud import ConversationCRUD

class ConversationMemoryStore:
    """
    Handles conversation memory and context for the AI companion
    """
    
    def __init__(self, user_id: int, max_memory_days: int = 30):
        self.user_id = user_id
        self.max_memory_days = max_memory_days
    
    def get_conversation_summary(self, days: int = 7) -> str:
        """Get a summary of recent conversations for context"""
        conversations = ConversationCRUD.get_user_conversations(
            self.user_id, 
            limit=50
        )
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_convs = [
            conv for conv in conversations 
            if conv.timestamp >= cutoff_date
        ]
        
        if not recent_convs:
            return "No recent conversations found."
        
        # Group conversations by day
        daily_summaries = {}
        for conv in recent_convs:
            date_key = conv.timestamp.date()
            if date_key not in daily_summaries:
                daily_summaries[date_key] = []
            daily_summaries[date_key].append(conv)
        
        # Create summary
        summary = f"Conversation summary for {self.user_id} (last {days} days):\n\n"
        
        for date, convs in sorted(daily_summaries.items(), reverse=True):
            summary += f"=== {date.strftime('%B %d, %Y')} ===\n"
            
            # Sentiment analysis for the day
            sentiments = [c.sentiment_score for c in convs if c.sentiment_score is not None]
            if sentiments:
                avg_sentiment = sum(sentiments) / len(sentiments)
                sentiment_desc = self._sentiment_to_description(avg_sentiment)
                summary += f"Overall mood: {sentiment_desc}\n"
            
            # Key topics/concerns
            topics = self._extract_topics(convs)
            if topics:
                summary += f"Topics discussed: {', '.join(topics)}\n"
            
            # Medication mentions
            med_mentions = self._extract_medication_mentions(convs)
            if med_mentions:
                summary += f"Medications mentioned: {', '.join(med_mentions)}\n"
            
            summary += "\n"
        
        return summary
    
    def get_important_context(self) -> Dict[str, Any]:
        """Get important contextual information about the user"""
        conversations = ConversationCRUD.get_user_conversations(self.user_id, limit=100)
        
        context = {
            "mood_patterns": self._analyze_mood_patterns(conversations),
            "medication_patterns": self._analyze_medication_patterns(conversations),
            "common_concerns": self._extract_common_concerns(conversations),
            "preferred_topics": self._extract_preferred_topics(conversations),
            "communication_style": self._analyze_communication_style(conversations)
        }
        
        return context
    
    def _sentiment_to_description(self, score: float) -> str:
        """Convert sentiment score to human-readable description"""
        if score > 0.6:
            return "Very positive"
        elif score > 0.2:
            return "Positive"
        elif score > -0.2:
            return "Neutral"
        elif score > -0.6:
            return "Somewhat negative"
        else:
            return "Concerning/negative"
    
    def _extract_topics(self, conversations: List) -> List[str]:
        """Extract main topics from conversations"""
        # Simple keyword extraction - could be enhanced with NLP
        topic_keywords = {
            "health": ["pain", "doctor", "hospital", "medicine", "sick", "health", "feel"],
            "family": ["family", "children", "grandchildren", "spouse", "daughter", "son"],
            "activities": ["walk", "exercise", "garden", "read", "watch", "hobby"],
            "sleep": ["sleep", "tired", "rest", "bed", "night"],
            "food": ["eat", "food", "hungry", "meal", "cook", "dinner", "lunch"],
            "social": ["friend", "visit", "call", "lonely", "social", "people"]
        }
        
        found_topics = set()
        all_text = " ".join([conv.message.lower() for conv in conversations])
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                found_topics.add(topic)
        
        return list(found_topics)
    
    def _extract_medication_mentions(self, conversations: List) -> List[str]:
        """Extract medication names mentioned in conversations"""
        medications = set()
        
        # Common medication keywords
        med_indicators = ["pill", "medication", "medicine", "dose", "tablet", "take", "prescribed"]
        
        for conv in conversations:
            text_lower = conv.message.lower()
            # If medication indicators are present, look for potential drug names
            if any(indicator in text_lower for indicator in med_indicators):
                # This is a simplified approach - in production, you'd use medical NLP
                words = text_lower.split()
                for word in words:
                    if len(word) > 4 and not word in ["medicine", "medication", "tablet", "prescribed"]:
                        # Basic filtering for potential medication names
                        medications.add(word.capitalize())
        
        return list(medications)[:5]  # Return top 5
    
    def _analyze_mood_patterns(self, conversations: List) -> Dict[str, Any]:
        """Analyze mood patterns over time"""
        if not conversations:
            return {}
        
        sentiments = [c.sentiment_score for c in conversations if c.sentiment_score is not None]
        if not sentiments:
            return {}
        
        return {
            "average_mood": sum(sentiments) / len(sentiments),
            "mood_trend": "improving" if sentiments[-5:] > sentiments[:5] else "stable",
            "total_conversations": len(conversations),
            "sentiment_distribution": {
                "positive": len([s for s in sentiments if s > 0.2]),
                "neutral": len([s for s in sentiments if -0.2 <= s <= 0.2]),
                "negative": len([s for s in sentiments if s < -0.2])
            }
        }
    
    def _analyze_medication_patterns(self, conversations: List) -> Dict[str, Any]:
        """Analyze medication-related conversation patterns"""
        med_conversations = [
            c for c in conversations 
            if c.conversation_type == "medication" or 
               any(word in c.message.lower() for word in ["medication", "pill", "medicine", "dose"])
        ]
        
        return {
            "medication_discussions": len(med_conversations),
            "recent_medication_concerns": len([
                c for c in med_conversations[-10:] 
                if c.sentiment_score and c.sentiment_score < -0.3
            ])
        }
    
    def _extract_common_concerns(self, conversations: List) -> List[str]:
        """Extract common concerns or recurring themes"""
        concern_keywords = {
            "pain": ["pain", "hurt", "ache", "sore"],
            "sleep": ["sleep", "insomnia", "tired", "rest"],
            "loneliness": ["lonely", "alone", "isolated", "miss"],
            "confusion": ["confused", "forgot", "remember", "memory"],
            "anxiety": ["worried", "anxious", "scared", "nervous"]
        }
        
        concerns = {}
        all_messages = " ".join([conv.message.lower() for conv in conversations])
        
        for concern, keywords in concern_keywords.items():
            count = sum(all_messages.count(keyword) for keyword in keywords)
            if count > 0:
                concerns[concern] = count
        
        # Return top concerns
        return sorted(concerns.keys(), key=lambda x: concerns[x], reverse=True)[:3]
    
    def _extract_preferred_topics(self, conversations: List) -> List[str]:
        """Extract topics the user seems to enjoy discussing"""
        positive_convs = [
            c for c in conversations 
            if c.sentiment_score and c.sentiment_score > 0.3
        ]
        
        return self._extract_topics(positive_convs)[:3]
    
    def _analyze_communication_style(self, conversations: List) -> Dict[str, Any]:
        """Analyze the user's communication preferences"""
        if not conversations:
            return {}
        
        total_chars = sum(len(conv.message) for conv in conversations)
        avg_message_length = total_chars / len(conversations)
        
        return {
            "average_message_length": avg_message_length,
            "prefers_short_messages": avg_message_length < 50,
            "total_conversations": len(conversations),
            "most_active_time": self._find_most_active_time(conversations)
        }
    
    def _find_most_active_time(self, conversations: List) -> str:
        """Find when the user is most active in conversations"""
        if not conversations:
            return "unknown"
        
        time_counts = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}
        
        for conv in conversations:
            hour = conv.timestamp.hour
            if 6 <= hour < 12:
                time_counts["morning"] += 1
            elif 12 <= hour < 17:
                time_counts["afternoon"] += 1
            elif 17 <= hour < 22:
                time_counts["evening"] += 1
            else:
                time_counts["night"] += 1
        
        return max(time_counts.keys(), key=lambda x: time_counts[x])
