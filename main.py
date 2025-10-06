import streamlit as st
import asyncio
import threading
import time
from datetime import datetime, timedelta
from app.database.models import create_tables
from app.scheduling.reminder_scheduler import ReminderScheduler
from frontend.dashboard import run_dashboard
from frontend.caregiver_portal import show_caregiver_dashboard
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
    
    # Portal selector in sidebar
    if "caregiver_id" not in st.session_state:
        with st.sidebar:
            st.header("🚪 Portal Selection")
            portal = st.radio("Choose portal:", ["👤 Patient Portal", "👨‍⚕️ Caregiver Portal"])
            
            if portal == "👨‍⚕️ Caregiver Portal":
                show_caregiver_dashboard()
                return
    
    # Run the appropriate dashboard
    if "caregiver_id" in st.session_state:
        show_caregiver_dashboard()
    else:
        run_dashboard()

if __name__ == "__main__":
    main()
