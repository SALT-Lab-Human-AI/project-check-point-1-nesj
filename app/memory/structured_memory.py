from utils.timezone_utils import now_central
"""
Structured memory helper for querying factual user data
Provides easy access to medications, preferences, health data, and daily logs
"""

import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from app.database.crud import (
    MedicationCRUD, UserCRUD, PersonalEventCRUD, 
    MedicationLogCRUD, ConversationCRUD
)


class StructuredMemory:
    """Helper for querying structured user data"""
    
    @staticmethod
    def get_medication_schedule(user_id: int) -> str:
        """
        Get user's medication schedule in readable format
        
        Args:
            user_id: User ID
        
        Returns:
            Formatted medication schedule
        """
        medications = MedicationCRUD.get_user_medications(user_id)
        
        if not medications:
            return "You don't have any medications scheduled."
        
        schedule = "Your medication schedule:\n\n"
        for med in medications:
            schedule += f"• {med.name} - {med.dosage}\n"
            schedule += f"  Frequency: {med.frequency}\n"
            
            if med.schedule_times:
                try:
                    times = json.loads(med.schedule_times)
                    schedule += f"  Times: {', '.join(times)}\n"
                except:
                    pass
            
            if med.instructions:
                schedule += f"  Instructions: {med.instructions}\n"
            
            schedule += "\n"
        
        return schedule
    
    @staticmethod
    def get_user_preferences(user_id: int) -> Dict:
        """
        Get user preferences and profile data
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary of user preferences
        """
        user = UserCRUD.get_user(user_id)
        
        if not user:
            return {}
        
        preferences = {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "emergency_contact": user.emergency_contact
        }
        
        if user.preferences:
            try:
                user_prefs = json.loads(user.preferences)
                preferences.update(user_prefs)
            except:
                pass
        
        return preferences
    
    @staticmethod
    def get_daily_logs(user_id: int, date: datetime = None) -> Dict:
        """
        Get daily activity logs (meals, medications, conversations)
        
        Args:
            user_id: User ID
            date: Date to retrieve (defaults to today)
        
        Returns:
            Dictionary with daily logs
        """
        if date is None:
            date = now_central()
        
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        # Get conversations for the day
        from app.database.models import get_session, Conversation, MedicationLog
        from sqlmodel import select
        
        logs = {
            "date": date.strftime('%Y-%m-%d'),
            "meals": [],
            "medications_taken": [],
            "activities": [],
            "conversations_count": 0
        }
        
        with get_session() as session:
            # Get conversations
            conv_query = select(Conversation).where(
                Conversation.user_id == user_id,
                Conversation.timestamp >= day_start,
                Conversation.timestamp < day_end
            )
            conversations = session.exec(conv_query).all()
            logs["conversations_count"] = len(conversations)
            
            # Extract meals and activities from conversations
            for conv in conversations:
                text = (conv.message + " " + conv.response).lower()
                
                # Look for meal mentions
                if "breakfast" in text:
                    logs["meals"].append("breakfast")
                if "lunch" in text:
                    logs["meals"].append("lunch")
                if "dinner" in text:
                    logs["meals"].append("dinner")
                
                # Look for activity mentions
                if any(word in text for word in ["walk", "exercise", "activity"]):
                    logs["activities"].append(conv.message)
            
            # Get medication logs
            med_query = select(MedicationLog).where(
                MedicationLog.user_id == user_id,
                MedicationLog.taken_time >= day_start,
                MedicationLog.taken_time < day_end,
                MedicationLog.status == "taken"
            )
            med_logs = session.exec(med_query).all()
            
            # Get medication details
            medications = MedicationCRUD.get_user_medications(user_id, active_only=False)
            med_dict = {med.id: med for med in medications}
            
            for log in med_logs:
                if log.medication_id in med_dict:
                    med = med_dict[log.medication_id]
                    logs["medications_taken"].append({
                        "name": med.name,
                        "dosage": med.dosage,
                        "time": log.taken_time.strftime('%I:%M %p')
                    })
        
        return logs
    
    @staticmethod
    def recall_specific_info(user_id: int, query_type: str, date: datetime = None) -> str:
        """
        Recall specific information based on query type
        
        Args:
            user_id: User ID
            query_type: Type of query ('breakfast', 'medications', 'schedule', etc.)
            date: Date to query (defaults to today)
        
        Returns:
            Relevant information as string
        """
        query_type = query_type.lower()
        
        if "medication" in query_type or "schedule" in query_type:
            return StructuredMemory.get_medication_schedule(user_id)
        
        elif any(meal in query_type for meal in ['breakfast', 'lunch', 'dinner', 'meal']):
            logs = StructuredMemory.get_daily_logs(user_id, date)
            if logs["meals"]:
                meals_str = ", ".join(logs["meals"])
                return f"Today you mentioned having: {meals_str}"
            else:
                return "I don't have any record of meals today. What did you eat?"
        
        elif "event" in query_type or "appointment" in query_type:
            events = PersonalEventCRUD.get_upcoming_events(user_id, days=30)
            if events:
                event_list = "\n".join([f"• {e.title} on {e.event_date.strftime('%B %d, %Y')}" for e in events[:5]])
                return f"Upcoming events:\n{event_list}"
            else:
                return "You don't have any upcoming events scheduled."
        
        else:
            return StructuredMemory.get_formatted_profile(user_id)
    
    @staticmethod
    def get_formatted_profile(user_id: int) -> str:
        """
        Get formatted user profile for AI context
        
        Args:
            user_id: User ID
        
        Returns:
            Formatted profile string
        """
        user = UserCRUD.get_user(user_id)
        
        if not user:
            return "User profile not found."
        
        profile = f"User Profile:\n"
        profile += f"Name: {user.name}\n"
        
        if user.preferences:
            try:
                prefs = json.loads(user.preferences)
                profile += f"Preferences: {json.dumps(prefs, indent=2)}\n"
            except:
                pass
        
        # Add medication summary
        medications = MedicationCRUD.get_user_medications(user_id)
        if medications:
            profile += f"\nActive Medications ({len(medications)}):\n"
            for med in medications:
                profile += f"  • {med.name} - {med.dosage}\n"
        
        return profile
