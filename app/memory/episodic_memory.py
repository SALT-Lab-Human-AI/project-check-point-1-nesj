"""
Episodic memory for daily summaries and pattern tracking
Uses extractive summarization without external APIs
"""

import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import Counter
import re

from app.database.models import get_session
from app.database.crud import ConversationCRUD
from sqlmodel import SQLModel, Field, Session, select


class DailySummary(SQLModel, table=True):
    """Store daily conversation summaries"""
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: datetime
    summary_text: str
    key_topics: str  # JSON string of main topics discussed
    mood_average: Optional[float] = None
    total_conversations: int = Field(default=0)
    medications_logged: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)


class EpisodicMemory:
    """Manages episodic memory with daily summaries"""
    
    def __init__(self):
        """Initialize episodic memory system"""
        self._create_table()
    
    def _create_table(self):
        """Ensure DailySummary table exists"""
        from app.database.models import engine
        SQLModel.metadata.create_all(engine)
    
    def generate_daily_summary(self, user_id: int, date: datetime = None) -> Optional[DailySummary]:
        """
        Generate a summary for a specific day
        
        Args:
            user_id: User ID
            date: Date to summarize (defaults to today)
        
        Returns:
            DailySummary object or None
        """
        if date is None:
            date = datetime.now()
        
        # Get start and end of day
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        # Get all conversations for the day
        from app.database.models import Conversation
        from app.database.models import get_session
        
        with get_session() as session:
            query = select(Conversation).where(
                Conversation.user_id == user_id,
                Conversation.timestamp >= day_start,
                Conversation.timestamp < day_end
            )
            conversations = session.exec(query).all()
        
        if not conversations:
            return None
        
        # Extract key information
        all_text = []
        mood_scores = []
        medications_count = 0
        
        for conv in conversations:
            all_text.append(conv.message)
            all_text.append(conv.response)
            
            if conv.sentiment_score is not None:
                mood_scores.append(conv.sentiment_score)
            
            if "medication" in conv.message.lower() or "medication" in conv.response.lower():
                medications_count += 1
        
        # Generate extractive summary
        summary_text = self._create_extractive_summary(all_text)
        
        # Extract key topics
        key_topics = self._extract_key_topics(all_text)
        
        # Calculate average mood
        avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else None
        
        # Create or update summary
        with get_session() as session:
            # Check if summary already exists
            existing_query = select(DailySummary).where(
                DailySummary.user_id == user_id,
                DailySummary.date >= day_start,
                DailySummary.date < day_end
            )
            existing_summary = session.exec(existing_query).first()
            
            if existing_summary:
                # Update existing
                existing_summary.summary_text = summary_text
                existing_summary.key_topics = json.dumps(key_topics)
                existing_summary.mood_average = avg_mood
                existing_summary.total_conversations = len(conversations)
                existing_summary.medications_logged = medications_count
                session.add(existing_summary)
                session.commit()
                session.refresh(existing_summary)
                return existing_summary
            else:
                # Create new
                summary = DailySummary(
                    user_id=user_id,
                    date=day_start,
                    summary_text=summary_text,
                    key_topics=json.dumps(key_topics),
                    mood_average=avg_mood,
                    total_conversations=len(conversations),
                    medications_logged=medications_count
                )
                session.add(summary)
                session.commit()
                session.refresh(summary)
                return summary
    
    def get_summary(self, user_id: int, date: datetime = None) -> Optional[DailySummary]:
        """
        Retrieve summary for a specific day
        
        Args:
            user_id: User ID
            date: Date to retrieve (defaults to today)
        
        Returns:
            DailySummary object or None
        """
        if date is None:
            date = datetime.now()
        
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        with get_session() as session:
            query = select(DailySummary).where(
                DailySummary.user_id == user_id,
                DailySummary.date >= day_start,
                DailySummary.date < day_end
            )
            return session.exec(query).first()
    
    def get_recent_summaries(self, user_id: int, days: int = 7) -> List[DailySummary]:
        """
        Get summaries for recent days
        
        Args:
            user_id: User ID
            days: Number of days to retrieve
        
        Returns:
            List of DailySummary objects
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with get_session() as session:
            query = select(DailySummary).where(
                DailySummary.user_id == user_id,
                DailySummary.date >= cutoff_date
            ).order_by(DailySummary.date.desc())
            return session.exec(query).all()
    
    def get_formatted_summary(self, user_id: int, date: datetime = None) -> str:
        """
        Get formatted summary text for AI context
        
        Args:
            user_id: User ID
            date: Date to summarize
        
        Returns:
            Formatted summary string
        """
        summary = self.get_summary(user_id, date)
        
        if not summary:
            return "No summary available for this day."
        
        date_str = summary.date.strftime('%B %d, %Y')
        topics = json.loads(summary.key_topics) if summary.key_topics else []
        
        text = f"Summary for {date_str}:\n"
        text += f"{summary.summary_text}\n\n"
        text += f"Key topics: {', '.join(topics)}\n"
        text += f"Total conversations: {summary.total_conversations}\n"
        
        if summary.mood_average is not None:
            mood_label = "positive" if summary.mood_average > 0.2 else "neutral" if summary.mood_average > -0.2 else "concerned"
            text += f"Overall mood: {mood_label}\n"
        
        return text
    
    def _create_extractive_summary(self, texts: List[str], num_sentences: int = 3) -> str:
        """
        Create extractive summary using frequency-based approach
        
        Args:
            texts: List of text strings
            num_sentences: Number of sentences to extract
        
        Returns:
            Summary text
        """
        # Combine all texts
        combined_text = " ".join(texts)
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', combined_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return "No significant content to summarize."
        
        # Simple frequency-based scoring
        word_freq = Counter()
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            word_freq.update([w for w in words if len(w) > 3])
        
        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = re.findall(r'\b\w+\b', sentence.lower())
            score = sum(word_freq[w] for w in words if len(w) > 3)
            sentence_scores[i] = score / (len(words) + 1)  # Normalize by length
        
        # Get top sentences
        top_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        top_indices.sort()  # Keep chronological order
        
        summary_sentences = [sentences[i] for i in top_indices if i < len(sentences)]
        return ". ".join(summary_sentences) + "."
    
    def _extract_key_topics(self, texts: List[str], top_n: int = 5) -> List[str]:
        """
        Extract key topics from texts
        
        Args:
            texts: List of text strings
            top_n: Number of topics to extract
        
        Returns:
            List of key topics
        """
        # Combine texts and extract keywords
        combined = " ".join(texts).lower()
        
        # Common health/care related keywords to look for
        topic_keywords = {
            'medication': ['medication', 'medicine', 'pill', 'dose', 'prescription'],
            'health': ['health', 'feeling', 'pain', 'symptom', 'doctor'],
            'mood': ['happy', 'sad', 'worried', 'anxious', 'good', 'bad'],
            'family': ['family', 'daughter', 'son', 'grandchild', 'visit'],
            'activities': ['walk', 'exercise', 'hobby', 'activity', 'book', 'music'],
            'meals': ['breakfast', 'lunch', 'dinner', 'food', 'eat', 'meal']
        }
        
        topics_found = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in combined for keyword in keywords):
                topics_found.append(topic)
        
        return topics_found[:top_n]
