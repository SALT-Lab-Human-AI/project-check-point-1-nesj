# Installation Guide

This guide will help you set up the Carely AI Companion project on your local machine.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj.git
cd project-check-point-1-nesj
```

2. Create and activate a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Required Dependencies

The project relies on the following key packages:

- FastAPI (>= 0.118.0) - Web framework
- Streamlit (>= 1.50.0) - User interface
- APScheduler (>= 3.11.0) - Task scheduling
- ChromaDB (>= 1.2.2) - Vector database
- Groq (>= 0.32.0) - LLM integration
- GTTS (>= 2.5.4) - Text-to-speech
- Additional dependencies listed in requirements.txt

## Environment Setup

1. Create a `.env` file in the root directory with the following variables:
```env
# API Keys
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
DATABASE_URL=sqlite:///carely.db

# Optional: Telegram Bot Configuration (if using notifications)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Running the Application

Start the Streamlit application:
```bash
streamlit run main.py
```

The application will be available at:
- Dashboard URL: http://localhost:8501

The application will automatically:
- Initialize the database
- Load sample data
- Start the reminder scheduler
- Launch the web interface

## Project Structure

```
.
├── app/
│   ├── agents/        # AI agent implementations
│   ├── api/          # API routes and endpoints
│   ├── auth/         # Authentication utilities
│   ├── database/     # Database models and operations
│   ├── memory/       # Memory management system
│   └── scheduling/   # Task scheduling
├── data/            # Data storage
├── frontend/        # Streamlit dashboard
└── utils/          # Utility functions
```

## Database Setup

The application uses SQLite by default. The database file `carely.db` will be created automatically when you first run the application.

## Troubleshooting

1. If you encounter package conflicts:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

2. Database connection issues:
- Ensure the `carely.db` file has proper permissions
- Check if the SQLite database path is correctly configured

## Additional Resources

- API Documentation (when server is running): http://localhost:8000/docs
- Project Documentation: See `docs/` directory

## Support

For issues and questions, please open an issue on the GitHub repository:
https://github.com/SALT-Lab-Human-AI/project-check-point-1-nesj/issues