from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import List, Optional
import json
from app.database.models import (
    get_session, User, Medication, Conversation, Reminder, 
    MedicationLog, CaregiverAlert
)

class UserCRUD:
    @staticmethod
    def create_user(name: str, email: str = None, phone: str = None, 
                   preferences: dict = None, emergency_contact: str = None) -> User:
        """Create a new user"""
        with get_session() as session:
            preferences_json = json.dumps(preferences) if preferences else None
            user = User(
                name=name,
                email=email,
                phone=phone,
                preferences=preferences_json,
                emergency_contact=emergency_contact
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        """Get user by ID"""
        with get_session() as session:
            return session.get(User, user_id)
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Get all users"""
        with get_session() as session:
            return session.exec(select(User)).all()

class MedicationCRUD:
    @staticmethod
    def create_medication(user_id: int, name: str, dosage: str, frequency: str,
                         schedule_times: List[str], instructions: str = None) -> Medication:
        """Create a new medication"""
        with get_session() as session:
            medication = Medication(
                user_id=user_id,
                name=name,
                dosage=dosage,
                frequency=frequency,
                schedule_times=json.dumps(schedule_times),
                instructions=instructions
            )
            session.add(medication)
            session.commit()
            session.refresh(medication)
            return medication
    
    @staticmethod
    def get_user_medications(user_id: int, active_only: bool = True) -> List[Medication]:
        """Get all medications for a user"""
        with get_session() as session:
            query = select(Medication).where(Medication.user_id == user_id)
            if active_only:
                query = query.where(Medication.active == True)
            return session.exec(query).all()
    
    @staticmethod
    def update_medication(medication_id: int, **kwargs) -> Optional[Medication]:
        """Update medication"""
        with get_session() as session:
            medication = session.get(Medication, medication_id)
            if medication:
                for key, value in kwargs.items():
                    setattr(medication, key, value)
                session.add(medication)
                session.commit()
                session.refresh(medication)
            return medication

class ConversationCRUD:
    @staticmethod
    def save_conversation(user_id: int, message: str, response: str,
                         sentiment_score: float = None, sentiment_label: str = None,
                         conversation_type: str = "general") -> Conversation:
        """Save a conversation"""
        with get_session() as session:
            conversation = Conversation(
                user_id=user_id,
                message=message,
                response=response,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                conversation_type=conversation_type
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation
    
    @staticmethod
    def get_user_conversations(user_id: int, limit: int = 50) -> List[Conversation]:
        """Get recent conversations for a user"""
        with get_session() as session:
            query = select(Conversation).where(
                Conversation.user_id == user_id
            ).order_by(Conversation.timestamp.desc()).limit(limit)
            return session.exec(query).all()
    
    @staticmethod
    def get_recent_sentiment_data(user_id: int, days: int = 7) -> List[Conversation]:
        """Get recent conversations with sentiment data"""
        with get_session() as session:
            cutoff_date = datetime.now() - timedelta(days=days)
            query = select(Conversation).where(
                Conversation.user_id == user_id,
                Conversation.timestamp >= cutoff_date,
                Conversation.sentiment_score.isnot(None)
            ).order_by(Conversation.timestamp.desc())
            return session.exec(query).all()

class ReminderCRUD:
    @staticmethod
    def create_reminder(user_id: int, reminder_type: str, title: str, message: str,
                       scheduled_time: datetime, medication_id: int = None) -> Reminder:
        """Create a new reminder"""
        with get_session() as session:
            reminder = Reminder(
                user_id=user_id,
                reminder_type=reminder_type,
                title=title,
                message=message,
                scheduled_time=scheduled_time,
                medication_id=medication_id
            )
            session.add(reminder)
            session.commit()
            session.refresh(reminder)
            return reminder
    
    @staticmethod
    def get_pending_reminders(user_id: int = None) -> List[Reminder]:
        """Get pending reminders"""
        with get_session() as session:
            query = select(Reminder).where(
                Reminder.completed == False,
                Reminder.scheduled_time <= datetime.now()
            )
            if user_id:
                query = query.where(Reminder.user_id == user_id)
            return session.exec(query).all()
    
    @staticmethod
    def complete_reminder(reminder_id: int) -> Optional[Reminder]:
        """Mark reminder as completed"""
        with get_session() as session:
            reminder = session.get(Reminder, reminder_id)
            if reminder:
                reminder.completed = True
                reminder.completed_at = datetime.now()
                session.add(reminder)
                session.commit()
                session.refresh(reminder)
            return reminder

class MedicationLogCRUD:
    @staticmethod
    def log_medication_taken(user_id: int, medication_id: int, scheduled_time: datetime,
                           taken_time: datetime = None, status: str = "taken",
                           notes: str = None) -> MedicationLog:
        """Log medication intake"""
        with get_session() as session:
            log = MedicationLog(
                user_id=user_id,
                medication_id=medication_id,
                scheduled_time=scheduled_time,
                taken_time=taken_time or datetime.now(),
                status=status,
                notes=notes
            )
            session.add(log)
            session.commit()
            session.refresh(log)
            return log
    
    @staticmethod
    def get_medication_adherence(user_id: int, days: int = 7) -> dict:
        """Get medication adherence statistics"""
        with get_session() as session:
            cutoff_date = datetime.now() - timedelta(days=days)
            query = select(MedicationLog).where(
                MedicationLog.user_id == user_id,
                MedicationLog.scheduled_time >= cutoff_date
            )
            logs = session.exec(query).all()
            
            total = len(logs)
            taken = len([log for log in logs if log.status == "taken"])
            missed = len([log for log in logs if log.status == "missed"])
            
            return {
                "total": total,
                "taken": taken,
                "missed": missed,
                "adherence_rate": (taken / total * 100) if total > 0 else 0,
                "logs": logs
            }

class CaregiverAlertCRUD:
    @staticmethod
    def create_alert(user_id: int, alert_type: str, title: str, description: str,
                    severity: str = "medium") -> CaregiverAlert:
        """Create a caregiver alert"""
        with get_session() as session:
            alert = CaregiverAlert(
                user_id=user_id,
                alert_type=alert_type,
                title=title,
                description=description,
                severity=severity
            )
            session.add(alert)
            session.commit()
            session.refresh(alert)
            return alert
    
    @staticmethod
    def get_unresolved_alerts(user_id: int = None) -> List[CaregiverAlert]:
        """Get unresolved alerts"""
        with get_session() as session:
            query = select(CaregiverAlert).where(CaregiverAlert.resolved == False)
            if user_id:
                query = query.where(CaregiverAlert.user_id == user_id)
            query = query.order_by(CaregiverAlert.created_at.desc())
            return session.exec(query).all()
    
    @staticmethod
    def resolve_alert(alert_id: int) -> Optional[CaregiverAlert]:
        """Resolve an alert"""
        with get_session() as session:
            alert = session.get(CaregiverAlert, alert_id)
            if alert:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                session.add(alert)
                session.commit()
                session.refresh(alert)
            return alert
