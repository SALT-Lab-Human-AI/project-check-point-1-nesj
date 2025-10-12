from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime, time
from typing import Optional, List
import sqlite3

# Database setup
DATABASE_URL = "sqlite:///carely.db"
engine = create_engine(DATABASE_URL, echo=False)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[str] = None  # JSON string for preferences
    emergency_contact: Optional[str] = None
    telegram_chat_id: Optional[str] = None  # Telegram chat ID for notifications
    user_type: str = Field(default="patient")  # patient, caregiver, admin
    password_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Medication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    dosage: str
    frequency: str  # e.g., "daily", "twice_daily", "weekly"
    schedule_times: str  # JSON string of times like ["09:00", "21:00"]
    instructions: Optional[str] = None
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    message: str
    response: str
    sentiment_score: Optional[float] = None  # -1 to 1 scale
    sentiment_label: Optional[str] = None  # positive, negative, neutral
    conversation_type: str = Field(default="general")  # general, checkin, medication
    timestamp: datetime = Field(default_factory=datetime.now)

class Reminder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    reminder_type: str  # medication, checkin, alert
    title: str
    message: str
    scheduled_time: datetime
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None
    medication_id: Optional[int] = Field(default=None, foreign_key="medication.id")
    created_at: datetime = Field(default_factory=datetime.now)

class MedicationLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    medication_id: int = Field(foreign_key="medication.id")
    scheduled_time: datetime
    taken_time: Optional[datetime] = None
    status: str = Field(default="pending")  # pending, taken, missed, skipped
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class CaregiverAlert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    alert_type: str  # medication_missed, mood_concern, emergency
    severity: str = Field(default="medium")  # low, medium, high
    title: str
    description: str
    resolved: bool = Field(default=False)
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

class CaregiverPatientAssignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    caregiver_id: int = Field(foreign_key="user.id")
    patient_id: int = Field(foreign_key="user.id")
    relationship: Optional[str] = None  # family, professional, friend
    notification_preferences: Optional[str] = None  # JSON string
    created_at: datetime = Field(default_factory=datetime.now)

class PersonalEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    event_type: str  # birthday, appointment, family_event, hobby, achievement
    title: str
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    recurring: bool = Field(default=False)
    importance: str = Field(default="medium")  # low, medium, high
    created_at: datetime = Field(default_factory=datetime.now)

def create_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session"""
    return Session(engine)
