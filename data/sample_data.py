import json
from datetime import datetime, timedelta, time
from app.database.models import create_tables
from app.database.crud import (
    UserCRUD, MedicationCRUD, ConversationCRUD, ReminderCRUD,
    MedicationLogCRUD, CaregiverAlertCRUD, CaregiverPatientCRUD, PersonalEventCRUD
)

def initialize_sample_data():
    """Initialize the database with sample data for testing"""
    
    # Check if data already exists
    existing_users = UserCRUD.get_all_users()
    if existing_users:
        print("Sample data already exists, skipping initialization")
        return
    
    try:
        print("Initializing sample data...")
        
        # Create sample users
        user1 = UserCRUD.create_user(
            name="Dorothy Johnson",
            email="dorothy.johnson@email.com",
            phone="555-0123",
            preferences={
                "language": "English",
                "contact_time": "Morning",
                "reminders_enabled": True,
                "preferred_topics": ["family", "gardening", "cooking"]
            },
            emergency_contact="John Johnson (Son) - 555-0124"
        )
        
        user2 = UserCRUD.create_user(
            name="Robert Chen",
            email="robert.chen@email.com",
            phone="555-0125",
            preferences={
                "language": "English",
                "contact_time": "Afternoon",
                "reminders_enabled": True,
                "preferred_topics": ["reading", "chess", "music"]
            },
            emergency_contact="Lisa Chen (Daughter) - 555-0126"
        )
        
        print(f"Created users: {user1.name} (ID: {user1.id}), {user2.name} (ID: {user2.id})")
        
        # Create sample caregivers
        caregiver1 = UserCRUD.create_user(
            name="Sarah Miller",
            email="sarah.miller@carely.com",
            phone="555-0200",
            user_type="caregiver",
            password="caregiver123",
            preferences={
                "notification_preferences": "email_and_sms"
            }
        )
        
        caregiver2 = UserCRUD.create_user(
            name="Dr. James Wilson",
            email="james.wilson@carely.com",
            phone="555-0201",
            user_type="caregiver",
            password="caregiver123",
            preferences={
                "notification_preferences": "email"
            }
        )
        
        print(f"Created caregivers: {caregiver1.name} (ID: {caregiver1.id}), {caregiver2.name} (ID: {caregiver2.id})")
        
        # Assign patients to caregivers
        CaregiverPatientCRUD.assign_patient(
            caregiver_id=caregiver1.id,
            patient_id=user1.id,
            relationship="family",
            notification_preferences={"alerts": True, "weekly_reports": True}
        )
        
        CaregiverPatientCRUD.assign_patient(
            caregiver_id=caregiver1.id,
            patient_id=user2.id,
            relationship="professional",
            notification_preferences={"alerts": True, "weekly_reports": True}
        )
        
        CaregiverPatientCRUD.assign_patient(
            caregiver_id=caregiver2.id,
            patient_id=user2.id,
            relationship="professional",
            notification_preferences={"alerts": True, "weekly_reports": False}
        )
        
        print("Created caregiver-patient assignments")
        
        # Create personal events for memory
        PersonalEventCRUD.create_event(
            user_id=user1.id,
            event_type="family_event",
            title="Grandson's Birthday",
            description="Tommy turns 10 years old",
            event_date=datetime.now() + timedelta(days=15),
            importance="high"
        )
        
        PersonalEventCRUD.create_event(
            user_id=user1.id,
            event_type="appointment",
            title="Doctor's Appointment",
            description="Regular checkup with Dr. Smith",
            event_date=datetime.now() + timedelta(days=7),
            importance="medium"
        )
        
        PersonalEventCRUD.create_event(
            user_id=user2.id,
            event_type="hobby",
            title="Chess Club Meeting",
            description="Weekly chess club at community center",
            event_date=datetime.now() + timedelta(days=3),
            recurring=True,
            importance="medium"
        )
        
        print("Created personal events")
        
        # Create sample medications for user1 (Dorothy)
        med1 = MedicationCRUD.create_medication(
            user_id=user1.id,
            name="Lisinopril",
            dosage="10mg",
            frequency="daily",
            schedule_times=["09:00"],
            instructions="Take with breakfast, monitor blood pressure"
        )
        
        med2 = MedicationCRUD.create_medication(
            user_id=user1.id,
            name="Metformin",
            dosage="500mg",
            frequency="twice_daily",
            schedule_times=["08:00", "20:00"],
            instructions="Take with meals to reduce stomach upset"
        )
        
        med3 = MedicationCRUD.create_medication(
            user_id=user1.id,
            name="Vitamin D",
            dosage="1000 IU",
            frequency="daily",
            schedule_times=["09:00"],
            instructions="Take with food for better absorption"
        )
        
        # Create sample medications for user2 (Robert)
        med4 = MedicationCRUD.create_medication(
            user_id=user2.id,
            name="Atorvastatin",
            dosage="20mg",
            frequency="daily",
            schedule_times=["21:00"],
            instructions="Take in the evening, avoid grapefruit"
        )
        
        med5 = MedicationCRUD.create_medication(
            user_id=user2.id,
            name="Aspirin",
            dosage="81mg",
            frequency="daily",
            schedule_times=["09:00"],
            instructions="Low-dose aspirin for heart health"
        )
        
        print(f"Created {5} sample medications")
        
        # Create sample conversations with varying sentiments
        sample_conversations_user1 = [
            {
                "message": "Good morning Carely! I slept well last night and I'm feeling pretty good today.",
                "response": "Good morning Dorothy! I'm so glad to hear you slept well and are feeling good today. That's wonderful news! How are you feeling about taking your medications this morning?",
                "sentiment_score": 0.7,
                "sentiment_label": "positive",
                "conversation_type": "checkin",
                "timestamp": datetime.now() - timedelta(hours=2)
            },
            {
                "message": "I took my Lisinopril and Vitamin D with breakfast. The Metformin I'll take tonight.",
                "response": "That's perfect, Dorothy! You're doing such a great job staying on top of your medications. Taking them with meals is exactly right. How has your appetite been lately?",
                "sentiment_score": 0.4,
                "sentiment_label": "positive",
                "conversation_type": "medication",
                "timestamp": datetime.now() - timedelta(hours=1, minutes=45)
            },
            {
                "message": "My grandson called me yesterday and we talked for an hour. It made me so happy!",
                "response": "Oh Dorothy, that's absolutely wonderful! Family connections are so precious. What did you and your grandson talk about? I love hearing about these special moments.",
                "sentiment_score": 0.8,
                "sentiment_label": "positive",
                "conversation_type": "general",
                "timestamp": datetime.now() - timedelta(days=1, hours=3)
            },
            {
                "message": "I'm feeling a bit lonely today. My usual walking group cancelled because of the weather.",
                "response": "I'm sorry to hear you're feeling lonely today, Dorothy. Weather can really affect our plans, can't it? Would you like to talk about what you're feeling? Sometimes sharing helps. Maybe we could think of some indoor activities you enjoy?",
                "sentiment_score": -0.4,
                "sentiment_label": "negative",
                "conversation_type": "general",
                "timestamp": datetime.now() - timedelta(days=2, hours=5)
            },
            {
                "message": "I've been having some trouble remembering things lately. Yesterday I couldn't remember if I took my morning pills.",
                "response": "Thank you for sharing that with me, Dorothy. Memory concerns can be worrying, and it's completely normal to feel concerned about this. For your medications, we can set up better tracking systems. Have you mentioned these memory concerns to your doctor?",
                "sentiment_score": -0.6,
                "sentiment_label": "negative",
                "conversation_type": "general",
                "timestamp": datetime.now() - timedelta(days=3, hours=2)
            }
        ]
        
        sample_conversations_user2 = [
            {
                "message": "Hi Carely, I had a great day reading in the park. The weather was perfect.",
                "response": "Hello Robert! That sounds like a lovely day. Reading in the park sounds so peaceful and enjoyable. What book were you reading? I'd love to hear about it.",
                "sentiment_score": 0.6,
                "sentiment_label": "positive",
                "conversation_type": "general",
                "timestamp": datetime.now() - timedelta(hours=4)
            },
            {
                "message": "I'm worried about my cholesterol levels. The doctor wants to see me again next month.",
                "response": "I understand why you might be feeling worried about that, Robert. It's natural to have concerns about health check-ups. The good news is that you're taking your Atorvastatin regularly, which should help. How have you been feeling overall?",
                "sentiment_score": -0.3,
                "sentiment_label": "negative",
                "conversation_type": "general",
                "timestamp": datetime.now() - timedelta(days=1, hours=6)
            },
            {
                "message": "I played chess online with my old colleague today. I won two games!",
                "response": "That's fantastic, Robert! Winning two chess games must feel great, especially against a good opponent. Chess is such a wonderful way to keep your mind sharp and stay connected with friends. Do you play regularly?",
                "sentiment_score": 0.7,
                "sentiment_label": "positive",
                "conversation_type": "general",
                "timestamp": datetime.now() - timedelta(days=2, hours=3)
            }
        ]
        
        # Save conversations
        for conv_data in sample_conversations_user1:
            ConversationCRUD.save_conversation(
                user_id=user1.id,
                message=conv_data["message"],
                response=conv_data["response"],
                sentiment_score=conv_data["sentiment_score"],
                sentiment_label=conv_data["sentiment_label"],
                conversation_type=conv_data["conversation_type"]
            )
        
        for conv_data in sample_conversations_user2:
            ConversationCRUD.save_conversation(
                user_id=user2.id,
                message=conv_data["message"],
                response=conv_data["response"],
                sentiment_score=conv_data["sentiment_score"],
                sentiment_label=conv_data["sentiment_label"],
                conversation_type=conv_data["conversation_type"]
            )
        
        print(f"Created {len(sample_conversations_user1) + len(sample_conversations_user2)} sample conversations")
        
        # Create sample medication logs (showing some adherence patterns)
        # Dorothy's medication logs - good adherence with a few missed doses
        for i in range(7):  # Last 7 days
            day = datetime.now() - timedelta(days=i)
            
            # Lisinopril (morning)
            morning_time = day.replace(hour=9, minute=0, second=0, microsecond=0)
            status = "taken" if i not in [1, 4] else "missed"  # Missed on day 1 and 4
            MedicationLogCRUD.log_medication_taken(
                user_id=user1.id,
                medication_id=med1.id,
                scheduled_time=morning_time,
                taken_time=morning_time + timedelta(minutes=15) if status == "taken" else None,
                status=status
            )
            
            # Metformin (morning and evening)
            morning_metformin = day.replace(hour=8, minute=0, second=0, microsecond=0)
            evening_metformin = day.replace(hour=20, minute=0, second=0, microsecond=0)
            
            MedicationLogCRUD.log_medication_taken(
                user_id=user1.id,
                medication_id=med2.id,
                scheduled_time=morning_metformin,
                taken_time=morning_metformin + timedelta(minutes=10) if i != 1 else None,
                status="taken" if i != 1 else "missed"
            )
            
            MedicationLogCRUD.log_medication_taken(
                user_id=user1.id,
                medication_id=med2.id,
                scheduled_time=evening_metformin,
                taken_time=evening_metformin + timedelta(minutes=5) if i not in [1, 4] else None,
                status="taken" if i not in [1, 4] else "missed"
            )
            
            # Vitamin D
            vitamin_d_time = day.replace(hour=9, minute=5, second=0, microsecond=0)
            MedicationLogCRUD.log_medication_taken(
                user_id=user1.id,
                medication_id=med3.id,
                scheduled_time=vitamin_d_time,
                taken_time=vitamin_d_time + timedelta(minutes=5),
                status="taken"  # Dorothy is consistent with vitamins
            )
        
        # Robert's medication logs - very good adherence
        for i in range(7):
            day = datetime.now() - timedelta(days=i)
            
            # Atorvastatin (evening)
            evening_time = day.replace(hour=21, minute=0, second=0, microsecond=0)
            MedicationLogCRUD.log_medication_taken(
                user_id=user2.id,
                medication_id=med4.id,
                scheduled_time=evening_time,
                taken_time=evening_time + timedelta(minutes=10),
                status="taken"
            )
            
            # Aspirin (morning)
            morning_aspirin = day.replace(hour=9, minute=0, second=0, microsecond=0)
            status = "taken" if i != 2 else "missed"  # Only missed once
            MedicationLogCRUD.log_medication_taken(
                user_id=user2.id,
                medication_id=med5.id,
                scheduled_time=morning_aspirin,
                taken_time=morning_aspirin + timedelta(minutes=5) if status == "taken" else None,
                status=status
            )
        
        print("Created sample medication logs")
        
        # Create some sample reminders
        ReminderCRUD.create_reminder(
            user_id=user1.id,
            reminder_type="checkin",
            title="Good Morning Check-in",
            message="Good morning Dorothy! How are you feeling today? Did you sleep well?",
            scheduled_time=datetime.now() + timedelta(hours=1)
        )
        
        ReminderCRUD.create_reminder(
            user_id=user1.id,
            reminder_type="medication",
            title="Evening Metformin Reminder",
            message="Hi Dorothy, it's time for your evening Metformin (500mg). Remember to take it with food!",
            scheduled_time=datetime.now() + timedelta(hours=8),
            medication_id=med2.id
        )
        
        ReminderCRUD.create_reminder(
            user_id=user2.id,
            reminder_type="medication",
            title="Evening Atorvastatin",
            message="Good evening Robert, time for your Atorvastatin (20mg). Remember to avoid grapefruit!",
            scheduled_time=datetime.now() + timedelta(hours=10),
            medication_id=med4.id
        )
        
        print("Created sample reminders")
        
        # Create some sample caregiver alerts
        CaregiverAlertCRUD.create_alert(
            user_id=user1.id,
            alert_type="mood_concern",
            title="Memory Concerns Expressed",
            description="Dorothy mentioned having trouble remembering things lately and specifically mentioned uncertainty about taking morning medications. She expressed concern about her memory in yesterday's conversation.",
            severity="medium"
        )
        
        CaregiverAlertCRUD.create_alert(
            user_id=user1.id,
            alert_type="medication_missed",
            title="Medication Adherence Pattern",
            description="Dorothy has missed several doses of Lisinopril and Metformin over the past week (adherence rate: 76%). Consider reviewing medication schedule or reminder system.",
            severity="medium"
        )
        
        CaregiverAlertCRUD.create_alert(
            user_id=user2.id,
            alert_type="health_concern",
            title="Health Anxiety",
            description="Robert expressed worry about upcoming cholesterol follow-up appointment. While taking medication regularly, he may benefit from reassurance about his health management.",
            severity="low"
        )
        
        print("Created sample caregiver alerts")
        
        print("✅ Sample data initialization complete!")
        print(f"   - Users created: {user1.name}, {user2.name}")
        print(f"   - Medications: 5 total")
        print(f"   - Conversations: {len(sample_conversations_user1) + len(sample_conversations_user2)} total")
        print(f"   - Medication logs: 7 days of sample data")
        print(f"   - Reminders: 3 active")
        print(f"   - Alerts: 3 for caregiver attention")
        
    except Exception as e:
        print(f"Error initializing sample data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Create tables first
    create_tables()
    # Initialize sample data
    initialize_sample_data()
