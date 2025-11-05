import streamlit as st
import threading
from dotenv import load_dotenv
from app.database.models import create_tables
from app.scheduling.reminder_scheduler import ReminderScheduler
from frontend.dashboard import run_dashboard
from data.sample_data import initialize_sample_data

# Load environment variables
load_dotenv()

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
        page_title="Carely - Your AI Companion",
        page_icon="❤️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Carely - Your caring AI companion for elderly care"
        }
    )
    
    # Force light theme with custom CSS
    st.markdown("""
        <style>
        /* Force light theme */
        :root {
            color-scheme: light !important;
        }
        
        /* Remove Streamlit's default header/toolbar */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Remove top padding from sidebar */
        [data-testid="stSidebar"] {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        /* Remove top padding from sidebar content */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        /* Remove top margin from first element in sidebar */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"]:first-child {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        /* Remove the sidebar header decorator */
        [data-testid="stSidebarHeader"] {
            display: none !important;
        }
        
        /* Remove ALL top padding/margin from main content */
        .main .block-container {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        [data-testid="stAppViewContainer"] main {
            padding-top: 0 !important;
        }
        
        /* Remove padding from main content blocks */
        .main [data-testid="stVerticalBlock"] {
            padding-top: 0 !important;
            gap: 0 !important;
        }
        
        /* Remove spacing from first element */
        .main [data-testid="stVerticalBlock"] > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize the app
    scheduler = initialize_app()
    
    # Run the patient dashboard
    run_dashboard()

if __name__ == "__main__":
    main()
