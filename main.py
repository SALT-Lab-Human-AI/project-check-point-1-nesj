import streamlit as st
import asyncio
import threading
import time
from datetime import datetime, timedelta
from app.database.models import create_tables
from app.scheduling.reminder_scheduler import ReminderScheduler
from frontend.dashboard import run_dashboard
from data.sample_data import initialize_sample_data

# Initialize the database and sample data on startup
@st.cache_resource
def initialize_app():
    """Initialize the application with database and sample data"""
    create_tables()
    initialize_sample_data()
    
    # Start the reminder scheduler in a separate thread
    scheduler = ReminderScheduler()
    scheduler_thread = threading.Thread(target=scheduler.start, daemon=True)
    scheduler_thread.start()
    
    return scheduler

def main():
    st.set_page_config(
        page_title="Carely - AI Companion for Elderly Care",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize the app
    scheduler = initialize_app()
    
    # Run the dashboard
    run_dashboard()

if __name__ == "__main__":
    main()
