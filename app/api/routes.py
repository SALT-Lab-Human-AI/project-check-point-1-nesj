from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from app.database.models import get_session, Session
from app.database.crud import (
    UserCRUD, MedicationCRUD, ConversationCRUD, ReminderCRUD,
    MedicationLogCRUD, CaregiverAlertCRUD
)
from app.agents.companion_agent import CompanionAgent
from app.memory.conversation_store import ConversationMemoryStore

app = FastAPI(title="Carely API", description="AI Companion for Elderly Care", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize companion agent
companion_agent = CompanionAgent()

# Pydantic models for API requests
class ChatMessage(BaseModel):
    user_id: int
    message: str
    conversation_type: str = "general"

class MedicationCreate(BaseModel):
    user_id: int
    name: str
    dosage: str
    frequency: str
    schedule_times: List[str]
    instructions: Optional[str] = None

class MedicationLog(BaseModel):
    user_id: int
    medication_id: int
    status: str = "taken"
    notes: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    emergency_contact: Optional[str] = None

class CustomReminder(BaseModel):
    user_id: int
    title: str
    message: str
    scheduled_time: datetime

# Dependency to get database session
def get_db_session():
    return get_session()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Carely API - AI Companion for Elderly Care"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

# User endpoints
@app.post("/users/")
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        new_user = UserCRUD.create_user(
            name=user.name,
            email=user.email,
            phone=user.phone,
            preferences=user.preferences,
            emergency_contact=user.emergency_contact
        )
        return {"message": "User created successfully", "user_id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/")
async def get_all_users():
    """Get all users"""
    try:
        users = UserCRUD.get_all_users()
        return {"users": [{"id": u.id, "name": u.name, "email": u.email} for u in users]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get user by ID"""
    try:
        user = UserCRUD.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoints
@app.post("/chat/")
async def chat_with_companion(message: ChatMessage):
    """Chat with the AI companion"""
    try:
        response = companion_agent.generate_response(
            user_id=message.user_id,
            user_message=message.message,
            conversation_type=message.conversation_type
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{user_id}")
async def get_chat_history(user_id: int, limit: int = 50):
    """Get chat history for a user"""
    try:
        conversations = ConversationCRUD.get_user_conversations(user_id, limit)
        return {
            "conversations": [
                {
                    "id": c.id,
                    "message": c.message,
                    "response": c.response,
                    "sentiment_score": c.sentiment_score,
                    "sentiment_label": c.sentiment_label,
                    "timestamp": c.timestamp,
                    "conversation_type": c.conversation_type
                }
                for c in conversations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Medication endpoints
@app.post("/medications/")
async def create_medication(medication: MedicationCreate):
    """Create a new medication"""
    try:
        new_med = MedicationCRUD.create_medication(
            user_id=medication.user_id,
            name=medication.name,
            dosage=medication.dosage,
            frequency=medication.frequency,
            schedule_times=medication.schedule_times,
            instructions=medication.instructions
        )
        return {"message": "Medication created successfully", "medication_id": new_med.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/medications/{user_id}")
async def get_user_medications(user_id: int):
    """Get all medications for a user"""
    try:
        medications = MedicationCRUD.get_user_medications(user_id)
        return {
            "medications": [
                {
                    "id": m.id,
                    "name": m.name,
                    "dosage": m.dosage,
                    "frequency": m.frequency,
                    "schedule_times": json.loads(m.schedule_times) if m.schedule_times else [],
                    "instructions": m.instructions,
                    "active": m.active
                }
                for m in medications
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/medications/log/")
async def log_medication_taken(log: MedicationLog):
    """Log medication intake"""
    try:
        medication_log = MedicationLogCRUD.log_medication_taken(
            user_id=log.user_id,
            medication_id=log.medication_id,
            scheduled_time=datetime.now(),
            status=log.status,
            notes=log.notes
        )
        return {"message": "Medication logged successfully", "log_id": medication_log.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/medications/adherence/{user_id}")
async def get_medication_adherence(user_id: int, days: int = 7):
    """Get medication adherence statistics"""
    try:
        adherence = MedicationLogCRUD.get_medication_adherence(user_id, days)
        return adherence
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reminder endpoints
@app.get("/reminders/{user_id}")
async def get_pending_reminders(user_id: int):
    """Get pending reminders for a user"""
    try:
        reminders = ReminderCRUD.get_pending_reminders(user_id)
        return {
            "reminders": [
                {
                    "id": r.id,
                    "type": r.reminder_type,
                    "title": r.title,
                    "message": r.message,
                    "scheduled_time": r.scheduled_time,
                    "medication_id": r.medication_id
                }
                for r in reminders
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reminders/{reminder_id}/complete")
async def complete_reminder(reminder_id: int):
    """Mark reminder as completed"""
    try:
        reminder = ReminderCRUD.complete_reminder(reminder_id)
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")
        return {"message": "Reminder completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Alert endpoints
@app.get("/alerts/{user_id}")
async def get_caregiver_alerts(user_id: int):
    """Get caregiver alerts for a user"""
    try:
        alerts = CaregiverAlertCRUD.get_unresolved_alerts(user_id)
        return {
            "alerts": [
                {
                    "id": a.id,
                    "type": a.alert_type,
                    "severity": a.severity,
                    "title": a.title,
                    "description": a.description,
                    "created_at": a.created_at,
                    "resolved": a.resolved
                }
                for a in alerts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: int):
    """Resolve a caregiver alert"""
    try:
        alert = CaregiverAlertCRUD.resolve_alert(alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "Alert resolved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Memory and context endpoints
@app.get("/memory/{user_id}/summary")
async def get_conversation_summary(user_id: int, days: int = 7):
    """Get conversation summary for a user"""
    try:
        memory_store = ConversationMemoryStore(user_id)
        summary = memory_store.get_conversation_summary(days)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/{user_id}/context")
async def get_important_context(user_id: int):
    """Get important contextual information about a user"""
    try:
        memory_store = ConversationMemoryStore(user_id)
        context = memory_store.get_important_context()
        return {"context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.get("/analytics/{user_id}/sentiment")
async def get_sentiment_trends(user_id: int, days: int = 30):
    """Get sentiment trends for a user"""
    try:
        conversations = ConversationCRUD.get_recent_sentiment_data(user_id, days)
        sentiment_data = [
            {
                "date": c.timestamp.date().isoformat(),
                "sentiment_score": c.sentiment_score,
                "sentiment_label": c.sentiment_label
            }
            for c in conversations
            if c.sentiment_score is not None
        ]
        return {"sentiment_trends": sentiment_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
