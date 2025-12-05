# Database Architecture & Usage Guide

## Overview

The Carely database layer uses SQLModel with SQLite for data persistence, implementing a connection pooling pattern with context managers for automatic resource cleanup.

## Connection Lifecycle

### Session Management

```python
# Get a session with automatic cleanup
with get_session() as session:
    # Database operations here
    session.add(item)
    session.commit()
# Session automatically closes after the block
```

Connection management is handled through the `get_session()` factory function, which ensures:
- Connections are pooled and reused
- Resources are properly cleaned up
- Transactions are automatically managed
- Sessions are thread-local

## CRUD Operations

The database layer is organized into CRUD classes for each entity type:

1. **UserCRUD**: User management operations
2. **MedicationCRUD**: Medication and schedule management
3. **ConversationCRUD**: Chat history and sentiment tracking
4. **ReminderCRUD**: Scheduled reminders and notifications
5. **MedicationLogCRUD**: Medication adherence tracking
6. **CaregiverAlertCRUD**: Alert system for caregivers
7. **PersonalEventCRUD**: Personal event and memory tracking

### Usage by Components

#### API Layer
- Uses CRUD operations for REST endpoints
- Maintains short-lived sessions per request
- Handles data validation and transformation

Example:
```python
@app.get("/users/{user_id}/medications")
def get_medications(user_id: int):
    medications = MedicationCRUD.get_user_medications(user_id)
    return medications
```

#### Agent Layer
- CompanionAgent uses CRUD for:
  - Conversation history
  - Medication tracking
  - Alert generation
  - Memory management

Example:
```python
def log_medication(self, user_id, medication_id):
    return MedicationLogCRUD.log_medication_taken(
        user_id=user_id,
        medication_id=medication_id
    )
```

#### Scheduler
- Uses CRUD for periodic tasks:
  - Medication reminders
  - Daily check-ins
  - Alert processing
  - Data cleanup

Example:
```python
def process_medication_reminders():
    reminders = ReminderCRUD.get_pending_reminders()
    for reminder in reminders:
        # Process reminder
```

## Best Practices

1. **Session Management**
   - Always use context managers (`with` statements)
   - Keep sessions short-lived
   - Commit transactions explicitly

2. **Error Handling**
   - Use try/except blocks around database operations
   - Roll back transactions on errors
   - Log database exceptions

3. **Query Optimization**
   - Use specific queries instead of loading full objects
   - Implement pagination for large result sets
   - Index frequently queried fields

4. **Data Integrity**
   - Use foreign key constraints
   - Validate data before insertion
   - Maintain referential integrity

## Models

The database uses SQLModel with the following core models:

- `User`: User profiles and authentication
- `Medication`: Medication schedules and instructions
- `Conversation`: Chat history and sentiment analysis
- `Reminder`: Scheduled notifications
- `MedicationLog`: Medication adherence tracking
- `CaregiverAlert`: Alert system
- `PersonalEvent`: Event and memory tracking

## Schema Updates

When updating the database schema:
1. Update model definitions in `models.py`
2. Create migration scripts if needed
3. Test migrations on development database
4. Back up production database before deploying changes