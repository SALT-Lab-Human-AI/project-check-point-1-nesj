# Carely - AI Companion for Elderly Care

## Overview

Carely is a comprehensive AI-powered elderly care companion application that provides proactive health monitoring, medication management, and emotional support. The system uses OpenAI's GPT-5 for natural language interactions, sentiment analysis, and emergency detection. It features a dual-portal architecture serving both patients and caregivers, with automated scheduling for medication reminders and wellness check-ins. The application stores conversation history and personal context to provide personalized, empathetic interactions while monitoring for concerning health patterns and alerting caregivers when necessary.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid UI development with minimal complexity
- **Portal Structure**: Dual-portal design with separate patient and caregiver interfaces
- **Session Management**: Streamlit session state for user authentication and context persistence
- **Visualization**: Plotly for interactive charts showing medication adherence trends and sentiment analysis
- **Voice Input**: Integrated speech-to-text capability using streamlit-mic-recorder for accessibility

**Rationale**: Streamlit was chosen for its simplicity and rapid development capabilities, allowing quick iteration on UI features. The dual-portal approach separates concerns between patient-facing companionship features and caregiver-facing analytics/monitoring tools.

### Backend Architecture
- **AI Agent System**: Central CompanionAgent class orchestrating all AI interactions using OpenAI GPT-5
- **Memory System**: ConversationMemoryStore provides context-aware conversations by retrieving and summarizing past interactions
- **Scheduling System**: APScheduler (BackgroundScheduler) handles automated reminders, check-ins, and reports
- **CRUD Pattern**: Separated data access layer with dedicated CRUD classes for each model (UserCRUD, MedicationCRUD, etc.)
- **Authentication**: Simple hash-based authentication (SHA-256) with role-based access control (patient/caregiver/admin hierarchy)

**Rationale**: The agent-based architecture centralizes AI logic for maintainability. The memory system enables personalized interactions by maintaining conversation context. Separation of scheduling into a background service ensures reminders execute reliably independent of user interactions.

### Data Storage
- **Database**: SQLite with SQLModel ORM for type-safe database operations
- **Schema Design**: 
  - Core entities: User, Medication, Conversation, Reminder, MedicationLog
  - Relationship tracking: CaregiverPatientAssignment links caregivers to patients
  - Alert system: CaregiverAlert for flagging concerning patterns
  - Personal context: PersonalEvent stores important life events and memories
- **JSON Fields**: Preferences, schedule times, and metadata stored as JSON strings for flexibility
- **Timestamps**: All critical entities track creation time for temporal analysis

**Rationale**: SQLite chosen for simplicity and zero-configuration deployment. SQLModel provides type safety and Pydantic validation. JSON fields allow schema flexibility without migrations for user-specific data structures.

### AI and Analytics Components
- **Conversation AI**: OpenAI GPT-5 with specialized system prompts for elderly-appropriate communication
- **Sentiment Analysis**: Dedicated SentimentAnalyzer class using GPT-5 to detect emotional states and concerning patterns
- **Emergency Detection**: EmergencyDetector class identifies medical emergencies in conversations with severity classification (high/medium/low)
- **Emergency Trigger System**: Real-time emergency detection in chat with interactive safety sheet UI
  - Detects concerning health symptoms (chest pain, dizziness, breathing issues, etc.)
  - Shows three-step safety sheet: emergency alert → action options → confirmation
  - Options: Contact caregiver via Telegram or self-resolve ("I Feel OK")
  - Session state management to prevent duplicate alerts
- **Context Building**: Multi-turn conversation context with medication history, personal events, and past interactions

**Rationale**: GPT-5 provides state-of-the-art language understanding crucial for empathetic elder care. Separate analyzer classes isolate different AI concerns (sentiment, emergency) for modularity and testing. Emergency trigger system provides immediate intervention options while respecting patient autonomy. Structured JSON responses from AI enable programmatic decision-making.

### Notification and Alert System
- **Emergency Alerts**: Real-time caregiver notifications triggered by emergency detection
- **Telegram Integration**: TelegramNotifier class for push notifications to caregivers
- **Alert Persistence**: CaregiverAlert database table maintains alert history
- **Scheduled Reminders**: Automated medication and wellness check-in notifications

**Rationale**: Multi-channel notification approach ensures critical alerts reach caregivers. Telegram chosen for its reliability and ease of integration. Database persistence enables alert tracking and pattern analysis.

## External Dependencies

### AI Services
- **OpenAI API**: GPT-5 model for conversation, sentiment analysis, and emergency detection
  - Requires: `OPENAI_API_KEY` environment variable
  - Usage: Companion chat, sentiment scoring, emergency classification
  - Models: gpt-5 (latest), gpt-4o-mini (fallback)

### Communication Services
- **Telegram Bot API**: Push notifications to caregivers
  - Requires: `TELEGRAM_BOT_TOKEN` environment variable
  - Usage: Emergency alerts, medication reminders, status updates
  - Stored: `telegram_chat_id` in User table per user/caregiver

### Python Packages
- **Core Framework**: 
  - `streamlit`: Web interface and session management
  - `fastapi`: REST API endpoints (routes.py)
- **Database**: 
  - `sqlmodel`: ORM and schema definition
  - `sqlite3`: Database engine (built-in)
- **AI/ML**:
  - `openai`: Official OpenAI Python client
  - `langchain`: (referenced in requirements but not actively used in codebase)
- **Scheduling**: 
  - `apscheduler`: Background job scheduling
- **Data Processing**:
  - `pandas`: Data manipulation for analytics
  - `plotly`: Interactive visualizations
- **Utilities**:
  - `requests`: HTTP client for Telegram API
  - `streamlit-mic-recorder`: Voice input component

### Database Schema
- **Primary Database**: `carely.db` (SQLite file)
- **Tables**: User, Medication, Conversation, Reminder, MedicationLog, CaregiverAlert, CaregiverPatientAssignment, PersonalEvent
- **No external database service required** - self-contained SQLite file

### Environment Configuration
Required environment variables:
- `OPENAI_API_KEY`: OpenAI API authentication
- `TELEGRAM_BOT_TOKEN`: Telegram bot authentication (optional for notifications)

### Sample Data System
- Initialization logic in `data/sample_data.py`
- Auto-populates users, medications, caregivers, and relationships on first run
- Checks for existing data to prevent duplication