"""Add personal events for Dorothy"""
from datetime import datetime, time
from app.database.models import get_session
from app.database.crud import UserCRUD, PersonalEventCRUD


def add_events_for_dorothy():
    """Add all personal events for Dorothy"""

    # Find Dorothy's user ID
    with get_session() as session:
        from sqlmodel import select
        from app.database.models import User
        result = session.exec(select(User).where(
            User.name.like('%Dorothy%'))).first()

        if not result:
            print("Dorothy not found in database")
            return

        user_id = result.id
        print(f"Found Dorothy with user_id: {user_id}")

    # Events to add (all moved to future dates: Dec 2025–Jan 2026)
    events = [
        # Health & Appointments
        {
            "user_id": user_id,
            "event_type": "appointment",
            "title": "Dentist Visit",
            "description": "Routine dental cleaning with Dr. Patel",
            # Next few days
            "event_date": datetime(2025, 12, 5, 10, 0),
            "recurring": False,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "appointment",
            "title": "Physical Therapy Session",
            "description":
            "Knee mobility exercises at Springfield Health Center",
            "event_date": datetime(2025, 12, 5, 14, 30),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "appointment",
            "title": "Eye Checkup",
            "description":
            "Follow-up with Dr. Green for new glasses prescription",
            "event_date": datetime(2025, 12, 6, 9, 15),
            "recurring": False,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "appointment",
            "title": "Blood Pressure Check",
            "description":
            "Local pharmacy health screening every Friday 9:00 AM",
            "event_date": datetime(2025, 12, 6, 9, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "appointment",
            "title": "Flu Shot Appointment",
            "description": "Clinic immunization visit",
            "event_date": datetime(2025, 12, 7, 11, 30),
            "recurring": False,
            "importance": "high"
        },

        # Family & Social Events
        {
            "user_id": user_id,
            "event_type": "family_event",
            "title": "Granddaughter's Dance Recital",
            "description": "Community theater",
            "event_date": datetime(2025, 12, 5, 18, 0),
            "recurring": False,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "family_event",
            "title": "Family Dinner",
            "description": "Sunday get-together at son's house",
            "event_date": datetime(2025, 12, 7, 17, 30),
            "recurring": True,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "family_event",
            "title": "Lunch with Mary",
            "description": "Catching up at the café",
            "event_date": datetime(2025, 12, 9, 12, 30),
            "recurring": False,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "family_event",
            "title": "Community Potluck",
            "description": "Neighborhood gathering",
            "event_date": datetime(2025, 12, 12, 13, 0),
            "recurring": False,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "family_event",
            "title": "Volunteer Meeting",
            "description": "Monthly seniors' club planning session",
            "event_date": datetime(2025, 12, 15, 15, 0),
            "recurring": True,
            "importance": "medium"
        },

        # Hobbies & Activities
        {
            "user_id": user_id,
            "event_type": "hobby",
            "title": "Morning Walk Group",
            "description": "Park walk with neighbors at 7:00 AM daily",
            "event_date": datetime(2025, 12, 5, 7, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "hobby",
            "title": "Chess Club Meeting",
            "description":
            "Weekly chess games at community center, Wednesdays 4:00 PM",
            "event_date": datetime(2025, 12, 10, 16, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "hobby",
            "title": "Knitting Circle",
            "description": "Craft meetup at library every Monday 2:00 PM",
            "event_date": datetime(2025, 12, 8, 14, 0),
            "recurring": True,
            "importance": "low"
        },
        {
            "user_id": user_id,
            "event_type": "hobby",
            "title": "Gardening Time",
            "description":
            "Water plants and prune garden every Tuesday & Friday 9:00 AM",
            "event_date": datetime(2025, 12, 9, 9, 0),
            "recurring": True,
            "importance": "low"
        },
        {
            "user_id": user_id,
            "event_type": "hobby",
            "title": "Yoga Class",
            "description": "Senior yoga class at local gym Thursdays 10:30 AM",
            "event_date": datetime(2025, 12, 11, 10, 30),
            "recurring": True,
            "importance": "medium"
        },

        # Personal Goals & Reminders
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Medication Refill Reminder",
            "description":
            "Refill blood pressure medication before next month",
            "event_date": datetime(2026, 1, 5, 9, 0),
            "recurring": False,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Check Mailbox",
            "description": "Remind daily at 5:00 PM",
            "event_date": datetime(2025, 12, 4, 17, 0),
            "recurring": True,
            "importance": "low"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Bill Payment Reminder",
            "description": "Pay electricity and phone bills",
            "event_date": datetime(2025, 12, 15, 9, 0),
            "recurring": False,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Weekly Meal Prep",
            "description": "Prepare Sunday meals for the week",
            "event_date": datetime(2025, 12, 7, 15, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Hydration Reminder",
            "description":
            "Drink a full glass of water every 3 hours between 8 AM–8 PM",
            "event_date": datetime(2025, 12, 4, 8, 0),
            "recurring": True,
            "importance": "low"
        },

        # Celebrations & Anniversaries
        {
            "user_id": user_id,
            "event_type": "birthday",
            "title": "Wedding Anniversary",
            "description": "Celebrate 45 years with a dinner",
            "event_date": datetime(2026, 1, 10, 18, 30),
            "recurring": True,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "birthday",
            "title": "Friend's Birthday",
            "description": "Call Linda to wish her happy birthday",
            "event_date": datetime(2026, 1, 3, 10, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "family_event",
            "title": "Thanksgiving Dinner",
            "description": "Family gathering planned",
            # Pushed into late January but still within ~2 months from early Dec
            "event_date": datetime(2026, 1, 25, 16, 0),
            "recurring": False,
            "importance": "high"
        },
        {
            "user_id": user_id,
            "event_type": "family_event",
            "title": "Neighborhood Festival",
            "description": "Attend local Fall Fest",
            "event_date": datetime(2026, 1, 10, 11, 0),
            "recurring": False,
            "importance": "medium"
        },

        # Routine & Wellness Tracking
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Morning Breakfast",
            "description": "Breakfast time at 8:00 AM",
            "event_date": datetime(2025, 12, 4, 8, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Lunch Time",
            "description": "Lunch at 12:30 PM",
            "event_date": datetime(2025, 12, 4, 12, 30),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Dinner Time",
            "description": "Dinner at 7:00 PM",
            "event_date": datetime(2025, 12, 4, 19, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Evening Gratitude Reflection",
            "description": "Write 3 good things before bed at 9:30 PM daily",
            "event_date": datetime(2025, 12, 4, 21, 30),
            "recurring": True,
            "importance": "low"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Weekly Weight Check",
            "description": "Track weight every Saturday morning",
            "event_date": datetime(2025, 12, 6, 9, 0),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Meditation Practice",
            "description":
            "10-minute guided breathing exercise every morning at 7:30 AM",
            "event_date": datetime(2025, 12, 4, 7, 30),
            "recurring": True,
            "importance": "medium"
        },
        {
            "user_id": user_id,
            "event_type": "hobby",
            "title": "Reading Hour",
            "description": "Read for 30 minutes after lunch at 1:00 PM daily",
            "event_date": datetime(2025, 12, 4, 13, 0),
            "recurring": True,
            "importance": "low"
        },
        {
            "user_id": user_id,
            "event_type": "achievement",
            "title": "Check Weather Forecast",
            "description": "Review forecast at 8:30 AM daily to plan walks",
            "event_date": datetime(2025, 12, 4, 8, 30),
            "recurring": True,
            "importance": "low"
        },
    ]

    # Add all events
    print(f"\nAdding {len(events)} personal events for Dorothy...")

    for event in events:
        try:
            PersonalEventCRUD.create_event(**event)
            print(f"✓ Added: {event['title']}")
        except Exception as e:
            print(f"✗ Failed to add {event['title']}: {str(e)}")

    print(f"\nComplete! All events added for Dorothy (user_id: {user_id})")

    # Verify
    all_events = PersonalEventCRUD.get_user_events(user_id, limit=100)
    print(f"\nTotal personal events for Dorothy: {len(all_events)}")


if __name__ == "__main__":
    add_events_for_dorothy()
