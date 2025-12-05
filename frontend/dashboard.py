import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, time
import json
import os
import requests
import time as time_module
import html
from typing import List, Dict, Any
from streamlit_mic_recorder import speech_to_text
from PIL import Image

from app.database.crud import (UserCRUD, MedicationCRUD, ConversationCRUD,
                               ReminderCRUD, MedicationLogCRUD,
                               CaregiverAlertCRUD, CaregiverPatientCRUD)
from app.agents.companion_agent import CompanionAgent
from utils.sentiment_analysis import analyze_sentiment, get_sentiment_emoji, get_sentiment_color
from utils.telegram_notification import send_emergency_alert
from utils.tts_helper import generate_speech_audio
from utils.timezone_utils import format_central_time, to_central, now_central


def apply_elderly_friendly_styling():
    """Apply modern health & wellness inspired CSS styling with optimized spacing"""
    st.markdown("""
        <style>
        /* Import modern fonts - Poppins and Inter for health app aesthetics */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
        
        /* CSS VARIABLES - Modern Health & Wellness Color Scheme */
        :root {
            /* Primary Colors - Inspired by Calm/Headspace */
            --primary-teal: #2D9CDB;
            --primary-green: #27AE60;
            --secondary-coral: #FF6B6B;
            --secondary-salmon: #E76F51;
            
            /* Backgrounds - Clean and airy */
            --bg-primary: #F8F9FA;
            --bg-secondary: #FDFDFD;
            --bg-card: #FFFFFF;
            
            /* Text Colors - High contrast for seniors */
            --text-primary: #2D3436;
            --text-secondary: #636E72;
            --text-muted: #95A5A6;
            
            /* Accent Colors - MyFitnessPal inspired */
            --accent-blue: #667EEA;
            --accent-lavender: #764BA2;
            --accent-mint: #4ECDC4;
            --accent-peach: #FFB88C;
            
            /* Status Colors - Traffic light system */
            --status-success: #27AE60;
            --status-warning: #F39C12;
            --status-danger: #E74C3C;
            --status-info: #3498DB;
            
            /* Event Colors - Color-coded categories */
            --event-medical: #5DADE2;
            --event-social: #F9E79F;
            --event-personal: #7DCEA0;
            
            /* Gradients - Calm/Headspace inspired */
            --gradient-header: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            --gradient-card-blue: linear-gradient(135deg, #E3F2FD 0%, #E8F5E9 100%);
            --gradient-card-peach: linear-gradient(135deg, #FFF3E0 0%, #FFE0E0 100%);
            --gradient-mood-positive: linear-gradient(135deg, #A8E6CF 0%, #7DCEA0 100%);
            --gradient-mood-neutral: linear-gradient(135deg, #FFE8B8 0%, #FFD89C 100%);
            --gradient-mood-concern: linear-gradient(135deg, #FFB8B8 0%, #FF9999 100%);
            
            /* Shadows - Subtle depth */
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
            
            /* Border Radius - Modern rounded corners */
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
        }
        
        /* Modern gradient background with wellness app feel */
        .stApp {
            background: linear-gradient(135deg, 
                #FFF5F7 0%,    /* Very light pink */
                #FFF9F5 25%,   /* Very light peach */
                #FFFEF5 50%,   /* Very light cream */
                #F5FFFA 75%,   /* Mint cream */
                #F8F5FF 100%   /* Very light lavender */
            ) !important;
            background-attachment: fixed !important;
        }
        
        /* ========== AGGRESSIVE WHITESPACE REDUCTION ========== */
        
        /* Remove ALL top spacing from main content */
        .main .block-container,
        [data-testid="stAppViewContainer"] .main .block-container,
        section.main > div,
        .block-container {
            padding-top: 0.5rem !important;
            margin-top: 0rem !important;
        }
        
        /* Remove spacing from element containers */
        .main .element-container:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Remove gap from vertical blocks */
        .main [data-testid="stVerticalBlock"]:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Global font settings - Inter for body */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 16px !important;
            line-height: 1.4 !important;
            color: #4A5568 !important;
        }
        
        /* Main content area - ULTRA COMPACT SPACING */
        .main {
            background: transparent !important;
            padding: 0.5rem 1rem !important;
        }
        
        .block-container {
            background: transparent !important;
            padding-top: 0.2rem !important;
            padding-bottom: 0.5rem !important;
            max-width: 1400px !important;
        }
        
        /* Headings - COMPACT SPACING */
        h1 {
            font-family: 'Poppins', sans-serif !important;
            font-size: 2rem !important;
            font-weight: 600 !important;
            color: #E08E7B !important;
            margin-bottom: 0.3rem !important;
            margin-top: 0 !important;
            line-height: 1.1 !important;
        }
        
        /* Force Carely header text color - override all other styles */
        .carely-header h1,
        .carely-header h2,
        .carely-header h1 *,
        .carely-header h2 *,
        div[style*="linear-gradient(135deg, #FF9A9E"] h1,
        div[style*="linear-gradient(135deg, #FF9A9E"] h2 {
            color: #1E3A8A !important;
        }
        
        h2 {
            font-family: 'Poppins', sans-serif !important;
            font-size: 1.4rem !important;
            font-weight: 600 !important;
            color: #D4A5A5 !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.3rem !important;
            line-height: 1.2 !important;
        }
        
        h3 {
            font-family: 'Poppins', sans-serif !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            color: #9DB4CE !important;
            margin-top: 0.3rem !important;
            margin-bottom: 0.2rem !important;
            line-height: 1.2 !important;
        }
        
        /* Paragraphs and text - COMPACT */
        p, .stMarkdown {
            font-size: 0.95rem !important;
            color: #4A5568 !important;
            line-height: 1.3 !important;
            margin-bottom: 0.3rem !important;
        }
        
        /* Sidebar styling - compact */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, 
                #FFF0F5 0%,    /* Lavender blush */
                #FFF9F0 50%,   /* Light peach */
                #F0F8FF 100%   /* Alice blue */
            ) !important;
            border-right: 2px solid rgba(224, 142, 123, 0.15) !important;
            padding-top: 1rem !important;
        }
        
        /* Buttons - compact with purple gradient styling */
        .stButton button {
            font-family: 'Poppins', sans-serif !important;
            font-size: 0.85rem !important;
            padding: 0.4rem 0.3rem !important;
            border-radius: 12px !important;
            min-height: 50px !important;
            margin: 0.1rem 0 !important;
        }
        
        /* Apply purple gradient to all secondary buttons across all sections */
        /* Style all secondary buttons with Carely gradient (matching Chat with Carely header) */
        button[kind="secondary"],
        .stButton button[kind="secondary"],
        .stButton button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 40%, #9FA8FF 100%) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 18px !important;
            font-family: "Inter", sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.07) !important;
            transition: all 0.3s ease !important;
        }
        
        /* Ensure button text and emojis are black and bold */
        button[kind="secondary"] *,
        .stButton button[kind="secondary"] * {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        
        button[kind="secondary"]:hover,
        .stButton button[kind="secondary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 14px rgba(0,0,0,0.10) !important;
        }
        
        button[kind="secondary"]:active,
        .stButton button[kind="secondary"]:active {
            transform: translateY(0px) !important;
        }
        
        /* Primary buttons (send button) */
        .stButton button[kind="primary"],
        .stButton button[data-testid="baseButton-primary"] {
            min-height: 45px !important;
            height: 45px !important;
            font-size: 1.2rem !important;
            padding: 0 1rem !important;
        }
        
        /* Text inputs - compact with light pink background and padding for mic button */
        .stTextInput input {
            font-size: 1rem !important;
            padding: 0.7rem 3.5rem 0.7rem 1rem !important; /* Extra right padding for mic button */
            border-radius: 12px !important;
            height: 45px !important;
            margin: 0.1rem 0 !important;
            background-color: #FFE8F6 !important;
            background: #FFE8F6 !important;
            border: 1px solid #FFB3D9 !important;
            color: #1A1A1A !important;
        }
        
        .stTextInput input::placeholder {
            color: #A0A6AF !important;
        }
        
        /* Make text input container relative for absolute positioning of mic */
        div[data-testid="stTextInput"] {
            position: relative !important;
            margin-bottom: 0 !important;
        }
        
        /* Target the parent container that wraps both text input and mic */
        div[data-testid="column"]:has(div[data-testid="stTextInput"]) {
            position: relative !important;
        }
        
        /* Chat messages - ULTRA COMPACT */
        .stChatMessage {
            font-size: 0.95rem !important;
            padding: 0.7rem 0.9rem !important;
            margin-bottom: 0.4rem !important;
            border-radius: 12px !important;
            line-height: 1.3 !important;
        }
        
        /* Metrics - COMPACT */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem !important;
        }
        
        /* Cards and containers - ULTRA COMPACT */
        .element-container {
            margin-bottom: 0.3rem !important;
        }
        
        /* Dividers - THIN */
        hr {
            margin: 0.5rem 0 !important;
            border: none !important;
            height: 1px !important;
        }
        
        /* Alert boxes - compact */
        .stSuccess, .stInfo, .stWarning, .stError {
            font-size: 0.95rem !important;
            padding: 0.8rem 1rem !important;
            border-radius: 10px !important;
            margin: 0.3rem 0 !important;
        }
        
        /* Summary cards - COMPACT */
        .summary-card {
            padding: 1rem !important;
            border-radius: 12px !important;
            height: 150px !important;
            margin: 0.2rem 0 !important;
        }
        
        .card-header {
            margin-bottom: 0.5rem !important;
        }
        
        .card-metric {
            font-size: 2.5rem !important;
            margin: 0.2rem 0 !important;
        }
        
        /* Event list - COMPACT */
        .event-item {
            padding: 0.6rem 0.8rem !important;
            margin-bottom: 0.3rem !important;
            border-radius: 8px !important;
        }
        
        .event-time {
            font-size: 0.9rem !important;
            margin-bottom: 0.1rem !important;
        }
        
        .event-title {
            font-size: 0.95rem !important;
            margin-bottom: 0.1rem !important;
        }
        
        /* Conversation cards - COMPACT */
        .conversation-card {
            padding: 0.7rem 0.9rem !important;
            margin-bottom: 0.4rem !important;
            border-radius: 10px !important;
        }
        
        /* Section headers - COMPACT */
        .section-header {
            margin: 0.5rem 0 0.3rem 0 !important;
            padding-bottom: 0.2rem !important;
        }
        
        /* Quick action buttons - COMPACT */
        .quick-actions-row {
            gap: 0.3rem !important;
            margin: 0.3rem 0 !important;
        }
        
        .quick-action-btn {
            min-height: 50px !important;
            font-size: 0.8rem !important;
            padding: 0.4rem 0.3rem !important;
        }
        
        /* Input area - COMPACT */
        .input-area {
            padding: 0.5rem 0 !important;
            margin-top: 0.3rem !important;
        }
        
        /* Remove all column padding */
        div[data-testid="column"] {
            padding: 0 0.2rem !important;
        }
        
        /* Vertical block spacing optimization */
        [data-testid="stVerticalBlock"] > div {
            gap: 0.2rem !important;
        }
        
        /* Remove excessive padding from markdown containers */
        [data-testid="stMarkdownContainer"] {
            padding: 0 !important;
        }
        
        /* Optimize expander spacing */
        .streamlit-expanderHeader {
            padding: 0.4rem 0.8rem !important;
            font-size: 0.95rem !important;
        }
        
        .streamlit-expanderContent {
            padding: 0.6rem 0.8rem !important;
        }
        
        /* Dataframe compact styling */
        .dataframe {
            font-size: 0.85rem !important;
        }
        
        .dataframe th {
            padding: 0.3rem !important;
            font-size: 0.8rem !important;
        }
        
        .dataframe td {
            padding: 0.2rem 0.3rem !important;
        }
        
        /* Reduce spacing in forms */
        .stForm {
            padding: 0.5rem !important;
        }
        
        /* Compact tabs */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 0.5rem !important;
        }
        
        /* Optimize image containers */
        [data-testid="stImage"] {
            margin: 0.3rem 0 !important;
        }
        
        /* Reduce spacing in alerts */
        .stAlert {
            padding: 0.6rem 0.8rem !important;
            margin: 0.3rem 0 !important;
        }
        
        /* Compact download buttons */
        .stDownloadButton button {
            padding: 0.4rem 0.8rem !important;
            min-height: 40px !important;
        }
        
        /* Optimize checkbox and radio spacing */
        .stCheckbox, .stRadio {
            margin-bottom: 0.2rem !important;
        }
        
        /* Compact date/time inputs */
        .stDateInput, .stTimeInput {
            margin-bottom: 0.3rem !important;
        }
        
        /* Text area optimization */
        .stTextArea textarea {
            line-height: 1.3 !important;
            padding: 0.6rem !important;
        }
        
        /* Number input compact */
        .stNumberInput input {
            padding: 0.4rem 0.6rem !important;
            height: 40px !important;
        }
        
        /* File uploader compact */
        .stFileUploader {
            padding: 0.5rem !important;
        }
        
        /* Slider spacing */
        .stSlider {
            padding: 0.3rem 0 !important;
        }
        
        /* Progress bar compact */
        .stProgress {
            margin: 0.3rem 0 !important;
        }
        
        /* Spinner compact */
        .stSpinner {
            margin: 0.5rem 0 !important;
        }
        
        /* Empty state styling - compact */
        .empty-state {
            padding: 1.5rem 1.5rem !important;
        }
        
        .empty-state-icon {
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .empty-state-title {
            font-size: 1.1rem !important;
            margin-bottom: 0.3rem !important;
        }
        
        /* Card grid system for better layout */
        .card-grid {
            gap: 0.5rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* Status badges - COMPACT */
        .status-badge {
            padding: 0.1rem 0.4rem !important;
            font-size: 0.7rem !important;
            margin-left: 0.2rem !important;
        }
        
        /* Grid layouts - COMPACT */
        .grid-container {
            gap: 0.4rem !important;
        }
        
        /* Caption text - SMALLER */
        .caption, [data-testid="stCaption"] {
            font-size: 0.75rem !important;
            margin-top: 0.1rem !important;
        }
        </style>
    """,
                unsafe_allow_html=True)


def format_time_central(dt: datetime, format_str: str = "%I:%M %p %Z") -> str:
    """Format datetime in Central Time for display"""
    if dt is None:
        return "N/A"
    return format_central_time(dt, format_str)


def run_dashboard():
    """Main dashboard function"""
    # Apply elderly-friendly styling
    apply_elderly_friendly_styling()

    # Initialize session state
    if 'companion_agent' not in st.session_state:
        st.session_state.companion_agent = CompanionAgent()

    # Sidebar for user selection and navigation
    with st.sidebar:
        # Display custom logo
        st.image("Logo.png", use_container_width=True)

        # Navigation with proper styling
        st.markdown("""
            <style>
            /* Fix navigation buttons to prevent text wrapping */
            div[role="radiogroup"] {
                gap: 0.3rem !important;
                width: 100% !important;
            }
            
            div[role="radiogroup"] label {
                border: 2px solid #E0E0E0 !important;
                border-radius: 10px !important;
                padding: 0.8rem 0.6rem !important;
                margin-bottom: 0.3rem !important;
                background: white !important;
                min-height: 50px !important;
                height: auto !important;
                display: flex !important;
                align-items: center !important;
                justify-content: flex-start !important;
                width: 100% !important;
                position: relative !important;
            }
            
            /* Hide the default text that appears outside */
            div[role="radiogroup"] label div {
                display: flex !important;
                align-items: center !important;
                gap: 0.6rem !important;
            }
            
            div[role="radiogroup"] label div p {
                display: inline-block !important;
                font-size: 1rem !important;
                font-weight: 500 !important;
                color: #2C3E50 !important;
                margin: 0 !important;
                padding: 0 !important;
                white-space: nowrap !important;
            }
            
            /* Radio button circles */
            div[role="radiogroup"] label input[type="radio"] {
                margin-right: 0.6rem !important;
                flex-shrink: 0 !important;
            }
            
            /* Hover state */
            div[role="radiogroup"] label:hover {
                border-color: #FF8C69 !important;
                background: #FFF5F2 !important;
                transform: translateX(3px);
            }
            
            /* Selected state - Use Carely gradient (matching Chat with Carely header) */
            div[role="radiogroup"] label[data-checked="true"] {
                border-color: transparent !important;
                background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 40%, #9FA8FF 100%) !important;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important;
            }
            
            div[role="radiogroup"] label[data-checked="true"] p {
                color: #111827 !important;
                font-weight: 600 !important;
            }
            
            /* Ensure sidebar has enough width */
            [data-testid="stSidebar"] {
                min-width: 280px !important;
            }
            </style>
        """,
                    unsafe_allow_html=True)

        # Navigation options
        page = st.radio("Navigate to:", [
            "🏠 Overview", "💬 Chat with Carely", "💊 Medications",
            "📊 Health Insights"
        ],
                        label_visibility="collapsed",
                        key="main_navigation")

    # Get user_id from session state
    selected_user_id = st.session_state.get('user_id',
                                            1)  # Default to 1 if not set

    # Main content based on selected page
    if page == "🏠 Overview":
        show_overview(selected_user_id)
    elif page == "💬 Chat with Carely":
        show_chat_interface(selected_user_id)
    elif page == "💊 Medications":
        show_medication_management(selected_user_id)
    elif page == "📊 Health Insights":
        show_health_insights(selected_user_id)


def get_daily_affirmation() -> str:
    """Generate ONE positive affirmation for the day using AI."""
    # ... (keep existing implementation, it's already compact)
    current_date = now_central().strftime('%Y-%m-%d')

    if 'daily_affirmation' not in st.session_state:
        st.session_state.daily_affirmation = {}

    if current_date in st.session_state.daily_affirmation:
        return st.session_state.daily_affirmation[current_date]

    fallback_affirmations = [
        "Today is a fresh start. You are doing wonderfully.",
        "Your presence brings joy to those around you.",
        "Each small step you take matters. You're doing great.",
        "You are valued, loved, and appreciated every day.",
        "Your wisdom and kindness make a real difference.",
    ]

    try:
        from groq import Groq
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            import random
            affirmation = random.choice(fallback_affirmations)
        else:
            client = Groq(api_key=groq_api_key)

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are a caring companion for seniors. Generate ONE short, positive affirmation."
                }, {
                    "role":
                    "user",
                    "content":
                    "Generate ONE positive affirmation for today. Keep it under 20 words, use simple language."
                }],
                temperature=0.8,
                max_tokens=50)

            affirmation = response.choices[0].message.content.strip()
            affirmation = affirmation.strip('"').strip("'")

            if len(affirmation.split()) > 20:
                import random
                affirmation = random.choice(fallback_affirmations)

    except Exception:
        import random
        affirmation = random.choice(fallback_affirmations)

    st.session_state.daily_affirmation[current_date] = affirmation
    return affirmation


def get_upcoming_events_for_overview(user_id: int) -> List[Dict[str, Any]]:
    """Get the next 10 upcoming personal events from the database."""
    # ... (keep existing implementation)
    events = []
    current_time = now_central()

    try:
        from app.database.models import PersonalEvent, get_session
        from sqlmodel import select

        with get_session() as session:
            query = select(PersonalEvent).where(
                PersonalEvent.user_id == user_id,
                PersonalEvent.event_date.isnot(None))
            personal_events = session.exec(query).all()

            for event in personal_events:
                event_time = to_central(event.event_date)

                if event_time >= current_time:
                    is_recurring = event.recurring if hasattr(
                        event, 'recurring') else False

                    emoji_map = {
                        'appointment': '📅',
                        'medication': '💊',
                        'birthday': '🎂',
                        'family_event': '👨‍👩‍👧‍👦',
                        'hobby': '🎨',
                        'achievement': '🏆',
                        'health': '🤖',
                        'social': '👥'
                    }
                    emoji = emoji_map.get(event.event_type, '📌')

                    events.append({
                        'datetime':
                        event_time,
                        'date_display':
                        event_time.strftime('%A, %B %d'),
                        'time_display':
                        event_time.strftime('%I:%M %p %Z'),
                        'emoji':
                        emoji,
                        'title':
                        event.title,
                        'description':
                        event.description or '',
                        'type':
                        event.event_type,
                        'is_recurring':
                        is_recurring
                    })
    except Exception:
        pass

    events.sort(key=lambda x: x['datetime'])
    return events[:10]


def show_overview(user_id: int):
    """Show overview dashboard with optimized spacing"""
    user = UserCRUD.get_user(user_id)
    if not user:
        st.error("User not found")
        return

    # Get current time in Central Time for display
    current_time = now_central()
    current_day = current_time.strftime("%A")
    current_date = current_time.strftime("%B %d, %Y")
    current_time_str = current_time.strftime("%I:%M %p %Z")

    # MODERN HEADER WITH CALM/HEADSPACE INSPIRED GRADIENT
    st.markdown("""
        <style>
        /* Force header text color with aggressive overrides - highest specificity */
        .carely-header h1,
        .carely-header h2,
        .carely-header h1 *,
        .carely-header h2 *,
        div.carely-header > h1,
        div.carely-header > h2,
        div[style*="linear-gradient(135deg, #FF9A9E"] h1,
        div[style*="linear-gradient(135deg, #FF9A9E"] h2,
        div[style*="linear-gradient(135deg, #FF9A9E"] h1 *,
        div[style*="linear-gradient(135deg, #FF9A9E"] h2 * {
            color: #1E3A8A !important;
        }
        
        /* Override global h1/h2 styles for header */
        .carely-header h1[style*="color"],
        .carely-header h2[style*="color"] {
            color: #1E3A8A !important;
        }
        </style>
        <div class="carely-header" style='background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 40%, #9FA8FF 100%);
                    text-align: center; 
                    margin: -1rem -1rem 1.5rem -1rem; 
                    padding: 2.5rem 1rem 2rem 1rem;
                    border-radius: 0 0 24px 24px;
                    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);'>
            <h1 class="carely-header-title" style='margin: 0; padding: 0; 
                       color: #1E3A8A !important; 
                       font-size: 2.8rem !important; 
                       font-weight: 700 !important; 
                       font-family: Poppins, sans-serif !important; 
                       line-height: 1.2 !important;
                       letter-spacing: -0.5px !important;
                       text-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;'>
                🌿 Carely: Your Wellness Companion
            </h1>
            <h2 class="carely-header-subtitle" style='margin: 0.6rem 0 0 0; 
                      font-size: 3.5rem !important; 
                      color: #1E3A8A !important; 
                      font-style: normal !important; 
                      font-family: Inter, sans-serif !important; 
                      line-height: 1.5 !important;
                      font-weight: 500 !important;'>
                Supporting your health journey, every step of the way ❤️
            </h2>
        </div>
        <style>
        /* Additional aggressive CSS for header text */
        .carely-header-title,
        .carely-header-subtitle,
        h1.carely-header-title,
        h2.carely-header-subtitle {
            color: #1E3A8A !important;
        }
        </style>
    """,
                unsafe_allow_html=True)

    # Separate JavaScript block to prevent rendering as text
    st.markdown("""
        <script>
        (function() {
            function forceHeaderColor() {
                const header = document.querySelector('.carely-header');
                if (header) {
                    const h1 = header.querySelector('h1, .carely-header-title');
                    const h2 = header.querySelector('h2, .carely-header-subtitle');
                    if (h1) {
                        h1.style.color = '#1E3A8A';
                        h1.style.setProperty('color', '#1E3A8A', 'important');
                        h1.querySelectorAll('*').forEach(el => {
                            el.style.color = '#1E3A8A';
                            el.style.setProperty('color', '#1E3A8A', 'important');
                        });
                    }
                    if (h2) {
                        h2.style.color = '#1E3A8A';
                        h2.style.setProperty('color', '#1E3A8A', 'important');
                        h2.querySelectorAll('*').forEach(el => {
                            el.style.color = '#1E3A8A';
                            el.style.setProperty('color', '#1E3A8A', 'important');
                        });
                    }
                }
                const allDivs = document.querySelectorAll('div[style*="linear-gradient(135deg, #FF9A9E"]');
                allDivs.forEach(div => {
                    const h1 = div.querySelector('h1');
                    const h2 = div.querySelector('h2');
                    if (h1) {
                        h1.style.color = '#1E3A8A';
                        h1.style.setProperty('color', '#1E3A8A', 'important');
                    }
                    if (h2) {
                        h2.style.color = '#1E3A8A';
                        h2.style.setProperty('color', '#1E3A8A', 'important');
                    }
                });
                document.querySelectorAll('.carely-header-title, .carely-header-subtitle').forEach(el => {
                    el.style.color = '#1E3A8A';
                    el.style.setProperty('color', '#1E3A8A', 'important');
                });
            }
            forceHeaderColor();
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', forceHeaderColor);
            } else {
                forceHeaderColor();
            }
            setTimeout(forceHeaderColor, 100);
            setTimeout(forceHeaderColor, 500);
            setTimeout(forceHeaderColor, 1000);
            setTimeout(forceHeaderColor, 2000);
            const observer = new MutationObserver(forceHeaderColor);
            observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class'] });
        })();
        </script>
    """,
                unsafe_allow_html=True)

    # ENHANCED WELCOME AND DATE/TIME SECTION - Top Row (2x2 Grid Layout)
    header_col1, header_col2 = st.columns([1, 1], gap="medium")

    with header_col1:
        welcome_html = f"""
<div style="background: linear-gradient(135deg, #E3F2FD 0%, #E8F5E9 100%); padding: 1rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 2px solid rgba(45, 156, 219, 0.15); height: 180px; min-height: 180px; max-height: 180px; display: flex; flex-direction: column; box-sizing: border-box; overflow: hidden;">
    <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.6rem; flex-shrink: 0;">
        <span style="font-size: 2rem;">👋</span>
        <h2 style="margin: 0; color: #2D3436; font-size: 1.4rem; font-weight: 700; font-family: Poppins, sans-serif; line-height: 1.2;">
            Hello, <span style="color: #2D9CDB; font-weight: 800;">{user.name}</span>!
        </h2>
    </div>
    <div style="background: linear-gradient(135deg, rgba(45, 156, 219, 0.12) 0%, rgba(78, 205, 196, 0.08) 100%); padding: 0.7rem 0.9rem; border-radius: 10px; border: 1.5px solid rgba(45, 156, 219, 0.2); box-shadow: 0 2px 8px rgba(45, 156, 219, 0.1); margin-top: auto; box-sizing: border-box; width: 100%;">
        <div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.3rem;">
            <span style="font-size: 1rem;">📅</span>
            <div style="font-size: 0.85rem; font-weight: 700; color: #2D9CDB; font-family: Poppins, sans-serif; letter-spacing: 0.2px;">
                {current_day}, {current_date}
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.4rem;">
            <span style="font-size: 0.9rem;">🕐</span>
            <div style="font-size: 0.8rem; color: #27AE60; font-weight: 600; font-family: Inter, sans-serif;">
                {current_time_str}
            </div>
        </div>
    </div>
</div>
"""
        st.markdown(welcome_html, unsafe_allow_html=True)

    with header_col2:
        daily_thought = get_daily_affirmation()
        inspiration_html = f"""
<div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0E0 100%); padding: 1.2rem; border-radius: 16px; height: 180px; min-height: 180px; max-height: 180px; box-shadow: 0 4px 16px rgba(255, 182, 140, 0.2); border: 2px solid rgba(255, 107, 107, 0.15); position: relative; overflow: hidden; display: flex; flex-direction: column; box-sizing: border-box;">
    <div style="position: absolute; top: 0.5rem; right: 0.8rem; font-size: 3rem; color: rgba(255, 107, 107, 0.08); font-family: Georgia, serif; line-height: 1;">
        "
    </div>
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; position: relative; z-index: 1; flex-shrink: 0;">
        <span style="font-size: 1.4rem;">✨</span>
        <span style="font-size: 1.2rem; font-weight: 700; color: #E76F51; font-family: Poppins, sans-serif; text-transform: uppercase; letter-spacing: 1px;">
            Daily Inspiration
        </span>
    </div>
    <div style="font-size: 1.1rem; line-height: 1.5; font-style: italic; color: #2D3436; font-family: Georgia, serif; font-weight: 500; position: relative; z-index: 1; text-shadow: 0 1px 2px rgba(255,255,255,0.5); flex: 1; display: flex; align-items: center;">
        "{daily_thought}"
    </div>
    <div style="position: absolute; bottom: 0.5rem; left: 0.8rem; font-size: 3rem; color: rgba(255, 107, 107, 0.08); font-family: Georgia, serif; line-height: 1; transform: rotate(180deg);">
        "
    </div>
</div>
"""
        st.markdown(inspiration_html, unsafe_allow_html=True)

    st.markdown("<div style='margin: 1.5rem 0;'></div>",
                unsafe_allow_html=True)

    # Today's summary cards - Bottom Row (2x2 Grid Layout)
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        # Medication adherence today
        current_time = now_central()
        medications = MedicationCRUD.get_user_medications(user_id)

        total_doses_scheduled = 0
        doses_taken = 0

        for med in medications:
            if not med.active or not med.schedule_times:
                continue

            try:
                schedule_times = json.loads(med.schedule_times) if isinstance(
                    med.schedule_times, str) else med.schedule_times

                for scheduled_time_str in schedule_times:
                    total_doses_scheduled += 1
                    scheduled_time = datetime.strptime(scheduled_time_str,
                                                       "%H:%M").time()
                    scheduled_datetime = datetime.combine(
                        current_time.date(), scheduled_time)
                    scheduled_datetime_central = to_central(scheduled_datetime)

                    today_logs = MedicationLogCRUD.get_today_medication_logs(
                        user_id=user_id, medication_id=med.id)

                    for log in today_logs:
                        if log.status != "taken":
                            continue

                        log_time = to_central(
                            log.taken_time) if log.taken_time else to_central(
                                log.scheduled_time)
                        log_minutes = log_time.hour * 60 + log_time.minute
                        scheduled_minutes = scheduled_time.hour * 60 + scheduled_time.minute

                        if len(schedule_times) == 1:
                            doses_taken += 1
                            break
                        else:
                            if abs(log_minutes - scheduled_minutes) <= 240:
                                doses_taken += 1
                                break
            except Exception:
                continue

        adherence_rate = (doses_taken / total_doses_scheduled *
                          100) if total_doses_scheduled > 0 else 0

        # COLOR CODED RECTANGULAR BOX - MyFitnessPal inspired traffic light system
        if adherence_rate >= 80:
            bg_color = "linear-gradient(135deg, #A8E6CF 0%, #7DCEA0 100%)"  # Success green gradient
            text_color = "#FFFFFF"
            status_emoji = "✅"
            status_text = "Excellent!"
        elif adherence_rate >= 50:
            bg_color = "linear-gradient(135deg, #FFE8B8 0%, #FFD89C 100%)"  # Warning yellow gradient
            text_color = "#8B5A00"
            status_emoji = "⚠️"
            status_text = "Keep it up"
        else:
            bg_color = "linear-gradient(135deg, #FFB8B8 0%, #FF9999 100%)"  # Alert red gradient
            text_color = "#FFFFFF"
            status_emoji = "💊"
            status_text = "Needs attention"

        st.markdown(f"""
            <div class='carely-metric-card carely-medication-card' style='background: {bg_color}; color: {text_color}; padding: 1.2rem 1rem; border-radius: 16px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 2px solid rgba(0,0,0,0.05); overflow: hidden;'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                    <span style='font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; opacity: 0.95; line-height: 1.3;'>Medication<br/>Adherence</span>
                    <span style='font-size: 1.8rem; flex-shrink: 0;'>💊</span>
                </div>
                <div style='text-align: center; padding: 0 0.5rem;'>
                    <div style='font-size: 2.6rem; font-weight: 800; line-height: 1; margin: 0.3rem 0; font-family: "Poppins", sans-serif;'>{int(adherence_rate)}%</div>
                    <div style='font-size: 1.1rem; opacity: 0.95; font-weight: 600; line-height: 1.4; margin-top: 0.3rem;'>{doses_taken} of {total_doses_scheduled} doses {status_emoji}</div>
                    <div style='font-size: 0.95rem; opacity: 0.9; margin-top: 0.25rem; font-weight: 500;'>{status_text}</div>
                </div>
            </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        # Enhanced mood card
        conversations = ConversationCRUD.get_recent_sentiment_data(user_id,
                                                                   days=1)
        if conversations:
            valid_sentiments = [
                c.sentiment_score for c in conversations
                if c.sentiment_score is not None
            ]

            if valid_sentiments:
                avg_mood = sum(valid_sentiments) / len(valid_sentiments)
                mood_emoji = get_sentiment_emoji(avg_mood)

                # COLOR CODED MOOD BOX - Headspace inspired emotional wellness colors
                if avg_mood > 0.3:
                    bg_color = "linear-gradient(135deg, #A8E6CF 0%, #7DCEA0 100%)"  # Positive mood green
                    text_color = "#FFFFFF"
                    mood_label = "Positive"
                    mood_icon = "😊"
                    status_text = "Feeling wonderful!"
                elif avg_mood > -0.3:
                    bg_color = "linear-gradient(135deg, #FFE8B8 0%, #FFD89C 100%)"  # Neutral mood yellow
                    text_color = "#8B5A00"
                    mood_label = "Balanced"
                    mood_icon = "😐"
                    status_text = "Doing well"
                else:
                    bg_color = "linear-gradient(135deg, #FFB8B8 0%, #FF9999 100%)"  # Concern mood red
                    text_color = "#FFFFFF"
                    mood_label = "Needs care"
                    mood_icon = "😔"
                    status_text = "We're here for you"

                st.markdown(f"""
                    <div class='carely-metric-card carely-mood-card' style='background: {bg_color}; color: {text_color}; padding: 1.2rem 1rem; border-radius: 16px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 2px solid rgba(0,0,0,0.05); overflow: hidden;'>
                        <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                            <span style='font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; opacity: 0.95;'>Today's Mood</span>
                            <span style='font-size: 1.8rem; flex-shrink: 0;'>💚</span>
                        </div>
                        <div style='text-align: center; padding: 0 0.5rem;'>
                            <div style='display: flex; align-items: center; justify-content: center; gap: 0.8rem;'>
                                <span style='font-size: 2.4rem; flex-shrink: 0;'>{mood_icon}</span>
                                <div>
                                    <div style='font-size: 2.4rem; font-weight: 800; line-height: 1; font-family: "Poppins", sans-serif;'>{avg_mood:.2f}</div>
                                    <div style='font-size: 1.1rem; font-weight: 700; margin-top: 0.2rem; line-height: 1.3;'>{mood_label}</div>
                                    <div style='font-size: 0.95rem; opacity: 0.9; margin-top: 0.2rem; font-weight: 500;'>{status_text}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                """,
                            unsafe_allow_html=True)
            else:
                # No sentiment data available
                st.markdown("""
                    <div class='carely-metric-card carely-mood-card' style='background: linear-gradient(135deg, #E0D0E0 0%, #D0C0D0 100%); color: #6B4C6B; padding: 1.2rem 1rem; border-radius: 16px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 2px solid rgba(0,0,0,0.05); overflow: hidden;'>
                        <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                            <span style='font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; opacity: 0.95;'>Today's Mood</span>
                            <span style='font-size: 1.8rem; flex-shrink: 0;'>💚</span>
                        </div>
                        <div style='text-align: center; padding: 0 0.5rem;'>
                            <div style='font-size: 2.2rem; margin-bottom: 0.4rem;'>💭</div>
                            <div style='font-size: 1.1rem; font-weight: 700; color: #5E35B1;'>No data yet</div>
                            <div style='font-size: 0.95rem; opacity: 0.85; margin-top: 0.2rem;'>Share how you feel today</div>
                        </div>
                    </div>
                """,
                            unsafe_allow_html=True)
        else:
            # No conversations at all
            st.markdown("""
                <div class='carely-metric-card carely-mood-card' style='background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%); color: #5E35B1; padding: 1.2rem 1rem; border-radius: 16px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 2px solid rgba(0,0,0,0.05); overflow: hidden;'>
                    <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                        <span style='font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; opacity: 0.95;'>Today's Mood</span>
                        <span style='font-size: 1.8rem; flex-shrink: 0;'>💙</span>
                    </div>
                    <div style='text-align: center; padding: 0 0.5rem;'>
                        <div style='font-size: 2.4rem; margin-bottom: 0.4rem;'>👋</div>
                        <div style='font-size: 1.1rem; font-weight: 700; color: #5E35B1; margin-top: 0.25rem;'>Begin your wellness journey</div>
                        <div style='font-size: 0.95rem; opacity: 0.9; margin-top: 0.2rem; font-weight: 500;'>Chat with Carely today</div>
                    </div>
                </div>
            """,
                        unsafe_allow_html=True)

    # Enhanced Events Section - COMPACT with tight spacing
    st.markdown("<div style='margin: 1rem 0 0.5rem 0;'></div>",
                unsafe_allow_html=True)
    st.markdown(
        "<h2 style='margin: 0 0 0.6rem 0; color: #2D9CDB; font-size: 1.9rem; font-weight: 700; font-family: Poppins, sans-serif; letter-spacing: -0.3px;'>🎯 Your Upcoming Schedule</h2>",
        unsafe_allow_html=True)

    upcoming_events = get_upcoming_events_for_overview(user_id)

    if upcoming_events:
        from collections import defaultdict
        events_by_date = defaultdict(list)
        for event in upcoming_events:
            events_by_date[event['date_display']].append(event)

        # Helper function for event colors
        def get_event_color(title):
            title_lower = title.lower()
            if any(word in title_lower for word in [
                    'doctor', 'medical', 'appointment', 'health', 'medication',
                    'clinic'
            ]):
                return '#5DADE2', '#E3F2FD'
            elif any(word in title_lower for word in
                     ['birthday', 'anniversary', 'family', 'visit']):
                return '#FF9966', '#FFF3E0'
            elif any(
                    word in title_lower for word in
                ['market', 'shopping', 'social', 'lunch', 'dinner', 'coffee']):
                return '#7DCEA0', '#E8F5E9'
            elif any(word in title_lower
                     for word in ['church', 'meeting', 'class', 'group']):
                return '#BB8FCE', '#F3E5F5'
            else:
                return '#2D9CDB', '#E3F2FD'

        # Render each date group and its events
        for date_str, date_events in events_by_date.items():
            # Date header - only show if multiple dates
            if len(events_by_date) > 1:
                st.markdown(
                    f"<div style='background: linear-gradient(135deg, rgba(45, 156, 219, 0.12) 0%, rgba(102, 126, 234, 0.1) 100%); padding: 0.5rem 1rem; border-radius: 10px; margin: 0.5rem 0 0.4rem 0; border-left: 4px solid #2D9CDB; box-shadow: 0 2px 6px rgba(45, 156, 219, 0.08);'><span style='font-size: 1.05rem; font-weight: 700; color: #2D3436; font-family: Poppins, sans-serif;'>📅 {date_str}</span></div>",
                    unsafe_allow_html=True)

            # Render each event as a complete card
            for event in date_events:
                event_color, event_card_bg = get_event_color(event['title'])
                description = event.get('description', '')
                if description and len(description) > 70:
                    description = description[:67] + "..."

                # Build date line for single-date view
                date_line = ""
                if len(events_by_date) == 1:
                    date_line = f"<div style='font-size: 0.75rem; color: #636E72; margin-top: 2px; font-weight: 600;'>{event['date_display']}</div>"

                # Build description HTML
                desc_html = ""
                if description:
                    desc_html = f"<div style='font-size: 0.9rem; color: #636E72; line-height: 1.4; margin-top: 0.2rem;'>{description}</div>"

                # Build recurring badge
                recurring_badge = ""
                if event.get('is_recurring'):
                    recurring_badge = "<div style='position: absolute; top: 0.6rem; right: 0.6rem;'><span style='background: linear-gradient(135deg, #BB8FCE 0%, #9B7EBD 100%); color: white; padding: 3px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;'>↻ Recurring</span></div>"

                # Padding adjustment for recurring badge
                content_padding = "70px" if event.get('is_recurring') else "0"

                # Complete event card - single line HTML
                event_html = f"<div style='background: linear-gradient(135deg, {event_card_bg} 0%, rgba(255,255,255,0.95) 100%); padding: 0.8rem 1rem; margin: 0 0 6px 0; border-radius: 10px; border-left: 4px solid {event_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.05); position: relative; display: flex; gap: 1rem; align-items: flex-start;'>{recurring_badge}<div style='min-width: 80px; text-align: center; flex-shrink: 0;'><div style='font-size: 1rem; font-weight: 800; color: {event_color}; line-height: 1.2;'>{event['time_display']}</div>{date_line}</div><div style='flex: 1; padding-right: {content_padding};'><div style='font-size: 1rem; font-weight: 700; color: #2D3436; line-height: 1.3;'><span style='font-size: 1.1rem; margin-right: 0.3rem;'>{event['emoji']}</span>{event['title']}</div>{desc_html}</div></div>"
                st.markdown(event_html, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #E3F2FD 0%, #E8F5E9 100%); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        text-align: center; 
                        border: 2px dashed rgba(45, 156, 219, 0.25);'>
                <div style='font-size: 2.2rem; margin-bottom: 0.3rem;'>📅</div>
                <div style='font-size: 1rem; font-weight: 600; color: #2D9CDB; margin-bottom: 0.3rem;'>Your schedule is clear</div>
                <div style='font-size: 0.85rem; color: #636E72;'>Add appointments to stay organized</div>
            </div>
        """,
                    unsafe_allow_html=True)

    # Enhanced Recent Conversations - COMPACT
    st.markdown("<div style='margin: 1.2rem 0 0.8rem 0;'></div>",
                unsafe_allow_html=True)
    st.markdown(
        "<h2 style='margin: 0; color: #764BA2; font-size: 1.9rem; font-weight: 700; font-family: Poppins, sans-serif; letter-spacing: -0.3px;'>💬 Your Recent Chats</h2>",
        unsafe_allow_html=True)

    recent_conversations = ConversationCRUD.get_user_conversations(user_id,
                                                                   limit=10)

    if recent_conversations:
        for conv in recent_conversations:
            sentiment_color = get_sentiment_color(conv.sentiment_score or 0)
            sentiment_emoji = get_sentiment_emoji(conv.sentiment_score or 0)
            display_time = to_central(conv.timestamp)

            user_msg = conv.message if len(
                conv.message) <= 60 else conv.message[:57] + "..."
            carely_msg = conv.response if len(
                conv.response) <= 140 else conv.response[:137] + "..."

            # Modern card-based conversation design
            conv_html = f"""
<div style='background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,249,250,0.95) 100%); 
            padding: 1rem 1.2rem; 
            margin-bottom: 10px; 
            border-radius: 12px; 
            border-left: 4px solid {sentiment_color}; 
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);'>
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;'>
        <div style='font-size: 0.85rem; font-weight: 700; color: #636E72; font-family: Inter, sans-serif; letter-spacing: 0.3px;'>
            {display_time.strftime('%I:%M %p')}
        </div>
        <div style='font-size: 1.3rem;'>{sentiment_emoji}</div>
    </div>
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
        <div style='background: rgba(45, 156, 219, 0.06); padding: 0.8rem 1rem; border-radius: 10px; border: 1px solid rgba(45, 156, 219, 0.15);'>
            <div style='font-size: 0.8rem; font-weight: 700; color: #2D9CDB; margin-bottom: 0.5rem; font-family: Poppins, sans-serif; text-transform: uppercase; letter-spacing: 0.5px;'>You</div>
            <div style='font-size: 0.95rem; color: #2D3436; line-height: 1.5; font-family: Inter, sans-serif;'>{user_msg}</div>
        </div>
        <div style='background: rgba(118, 75, 162, 0.06); padding: 0.8rem 1rem; border-radius: 10px; border: 1px solid rgba(118, 75, 162, 0.15);'>
            <div style='font-size: 0.8rem; font-weight: 700; color: #764BA2; margin-bottom: 0.5rem; font-family: Poppins, sans-serif; text-transform: uppercase; letter-spacing: 0.5px;'>Carely</div>
            <div style='font-size: 0.95rem; color: #2D3436; line-height: 1.5; font-family: Inter, sans-serif;'>{carely_msg}</div>
        </div>
    </div>
</div>
"""
            st.markdown(conv_html, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FFF3E0 0%, #F3E5F5 100%); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        text-align: center; 
                        border: 2px dashed rgba(118, 75, 162, 0.25);'>
                <div style='font-size: 2.2rem; margin-bottom: 0.3rem;'>💬</div>
                <div style='font-size: 1rem; font-weight: 600; color: #764BA2; margin-bottom: 0.3rem;'>Start your first conversation</div>
                <div style='font-size: 0.85rem; color: #636E72;'>Chat with Carely to track your wellness journey</div>
            </div>
        """,
                    unsafe_allow_html=True)


# ... (keep the rest of the functions like show_chat_interface, show_medication_management, etc.
# but apply similar compact spacing principles to them)


def show_emergency_safety_sheet(user_id: int, concerns: list, severity: str,
                                message: str):
    """Display emergency safety sheet with two-step flow"""
    user = UserCRUD.get_user(user_id)

    st.error("🚨 **EMERGENCY ALERT DETECTED**")

    st.markdown("### Safety Check")
    st.warning(f"We noticed you mentioned: {', '.join(concerns)}")

    st.markdown("---")
    st.markdown("### 📋 **What would you like to do?**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔴 **Notify Caregiver** (very urgent)",
                     use_container_width=True,
                     type="primary"):
            caregivers = CaregiverPatientCRUD.get_patient_caregivers(user_id)
            alert_sent = False

            if caregivers:
                for caregiver in caregivers:
                    if caregiver.telegram_chat_id:
                        result = send_emergency_alert(
                            chat_id=caregiver.telegram_chat_id,
                            patient_name=user.name,
                            concerns=concerns,
                            severity=severity,
                            message=message)
                        if result.get("success"):
                            alert_sent = True

            if not alert_sent and os.getenv("TELEGRAM_CHAT_ID"):
                result = send_emergency_alert(
                    chat_id=os.getenv("TELEGRAM_CHAT_ID"),
                    patient_name=user.name,
                    concerns=concerns,
                    severity=severity,
                    message=message)
                if result.get("success"):
                    alert_sent = True

            if alert_sent:
                st.success("✅ **Help is on the way!**")
                st.info(
                    "Your caregiver has been notified via Telegram and will be with you shortly."
                )
                st.session_state.emergency_handled = True
            else:
                st.warning(
                    "⚠️ We couldn't send the Telegram alert. Please call your caregiver directly."
                )
                st.info("📞 Emergency: 911")

    with col2:
        if st.button("🟢 **I feel OK** (manageable)", use_container_width=True):
            st.success("**Feeling better!**")
            st.info("That's great to hear! Are you feeling better?")
            st.session_state.emergency_handled = True

    st.markdown("---")
    st.caption(
        "💡 If this is a medical emergency, please call 911 immediately.")


def show_memory_game():
    """Senior-friendly Memory Card Matching Game"""
    import random

    st.header("🎮 Memory Card Game")
    st.markdown("### Match the pairs! Flip two cards to find matching pairs.")

    # Initialize game state
    if 'game_level' not in st.session_state:
        st.session_state.game_level = 1
    if 'game_deck' not in st.session_state:
        st.session_state.game_deck = []
    if 'revealed_cards' not in st.session_state:
        st.session_state.revealed_cards = []
    if 'matched_cards' not in st.session_state:
        st.session_state.matched_cards = set()
    if 'moves_count' not in st.session_state:
        st.session_state.moves_count = 0
    if 'game_start_time' not in st.session_state:
        st.session_state.game_start_time = None
    if 'game_theme' not in st.session_state:
        st.session_state.game_theme = "animals"
    if 'check_mismatch' not in st.session_state:
        st.session_state.check_mismatch = False

    # Themes with emojis
    themes = {
        "animals":
        ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸"],
        "fruits":
        ["🍎", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍑", "🍒", "🍍", "🥝", "🥭", "🍐", "🥥"],
        "flowers": [
            "🌸", "🌺", "🌻", "🌷", "🌹", "🥀", "🌼", "🏵️", "💐", "🌲", "🌳", "🌴", "🌱",
            "🍀"
        ]
    }

    # Determine grid size based on level
    level_config = {
        1: {
            "pairs": 2,
            "grid": (2, 2)
        },  # 4 cards
        2: {
            "pairs": 4,
            "grid": (2, 4)
        },  # 8 cards
        3: {
            "pairs": 6,
            "grid": (3, 4)
        },  # 12 cards
        4: {
            "pairs": 8,
            "grid": (4, 4)
        }  # 16 cards
    }

    current_config = level_config.get(st.session_state.game_level,
                                      level_config[1])
    pairs_needed = current_config["pairs"]
    grid_rows, grid_cols = current_config["grid"]

    def initialize_deck():
        """Create and shuffle deck"""
        theme_emojis = themes[st.session_state.game_theme]
        selected_emojis = theme_emojis[:pairs_needed]
        deck = selected_emojis * 2  # Create pairs
        random.shuffle(deck)
        return deck

    # Initialize deck if needed
    if not st.session_state.game_deck or len(
            st.session_state.game_deck) != pairs_needed * 2:
        st.session_state.game_deck = initialize_deck()
        st.session_state.revealed_cards = []
        st.session_state.matched_cards = set()
        st.session_state.moves_count = 0
        st.session_state.game_start_time = time_module.time()
        st.session_state.check_mismatch = False

    # Calculate elapsed time
    elapsed_time = 0
    if st.session_state.game_start_time:
        elapsed_time = int(time_module.time() -
                           st.session_state.game_start_time)

    # HUD - Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Level", st.session_state.game_level)
    with col2:
        st.metric("✨ Pairs Found",
                  f"{len(st.session_state.matched_cards)}/{pairs_needed}")
    with col3:
        st.metric("🔄 Moves", st.session_state.moves_count)
    with col4:
        st.metric("⏱️ Time", f"{elapsed_time}s")

    st.markdown("---")

    # Check if game is won
    if len(st.session_state.matched_cards) == pairs_needed:
        st.success(
            f"🎉 Congratulations! You completed Level {st.session_state.game_level}!"
        )
        st.balloons()

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.game_level < 4:
                if st.button("➡️ Next Level",
                             key="next_level",
                             use_container_width=True):
                    st.session_state.game_level += 1
                    st.session_state.game_deck = []
                    st.rerun()
            else:
                st.info("🏆 You've completed all levels!")

        with col2:
            if st.button("🔄 Restart Level",
                         key="restart_same",
                         use_container_width=True):
                st.session_state.game_deck = []
                st.rerun()

        with col3:
            if st.button("🏠 Back to Chat",
                         key="back_to_chat_win",
                         use_container_width=True):
                st.session_state.show_memory_game = False
                st.rerun()
        return

    # Game controls
    st.markdown("### 🎴 Game Board")
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        if st.button("🔄 Restart Level",
                     key="restart_game",
                     use_container_width=True):
            st.session_state.game_deck = []
            st.rerun()

    with col2:
        theme_options = list(themes.keys())
        selected_theme = st.selectbox("Theme",
                                      theme_options,
                                      index=theme_options.index(
                                          st.session_state.game_theme),
                                      key="theme_select")
        if selected_theme != st.session_state.game_theme:
            st.session_state.game_theme = selected_theme
            st.session_state.game_deck = []
            st.rerun()

    with col3:
        if st.button("🏠 Back to Chat",
                     key="back_to_chat",
                     use_container_width=True):
            st.session_state.show_memory_game = False
            st.rerun()

    st.markdown("---")

    # Handle mismatch delay (flip back after showing)
    if st.session_state.check_mismatch and len(
            st.session_state.revealed_cards) == 2:
        idx1, idx2 = st.session_state.revealed_cards
        if st.session_state.game_deck[idx1] != st.session_state.game_deck[
                idx2]:
            time_module.sleep(1.2)  # Show mismatch for 1.2 seconds
            st.session_state.revealed_cards = []
            st.session_state.check_mismatch = False
            st.rerun()

    # Render card grid
    for row in range(grid_rows):
        cols = st.columns(grid_cols)
        for col_idx in range(grid_cols):
            card_idx = row * grid_cols + col_idx

            with cols[col_idx]:
                # Check if card is matched or revealed
                is_matched = card_idx in st.session_state.matched_cards
                is_revealed = card_idx in st.session_state.revealed_cards

                if is_matched:
                    # Matched card - show emoji and disable
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%); 
                                    padding: 2rem; border-radius: 15px; text-align: center;
                                    font-size: 3rem; min-height: 120px; display: flex;
                                    align-items: center; justify-content: center;
                                    opacity: 0.7;'>
                            {st.session_state.game_deck[card_idx]}
                        </div>
                    """,
                                unsafe_allow_html=True)
                elif is_revealed:
                    # Revealed card - show emoji
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #FF8C69 0%, #FF6B47 100%); 
                                    padding: 2rem; border-radius: 15px; text-align: center;
                                    font-size: 3rem; min-height: 120px; display: flex;
                                    align-items: center; justify-content: center;
                                    box-shadow: 0 4px 12px rgba(255, 140, 105, 0.4);'>
                            {st.session_state.game_deck[card_idx]}
                        </div>
                    """,
                                unsafe_allow_html=True)
                else:
                    # Facedown card - clickable
                    if st.button("❓",
                                 key=f"card_{card_idx}",
                                 use_container_width=True):
                        # Can only reveal if less than 2 cards are shown
                        if len(st.session_state.revealed_cards) < 2:
                            st.session_state.revealed_cards.append(card_idx)

                            # Check if two cards are revealed
                            if len(st.session_state.revealed_cards) == 2:
                                st.session_state.moves_count += 1
                                idx1, idx2 = st.session_state.revealed_cards

                                # Check if they match
                                if st.session_state.game_deck[
                                        idx1] == st.session_state.game_deck[
                                            idx2]:
                                    # Match found!
                                    st.session_state.matched_cards.add(idx1)
                                    st.session_state.matched_cards.add(idx2)
                                    st.session_state.revealed_cards = []
                                else:
                                    # Mismatch - will flip back after delay
                                    st.session_state.check_mismatch = True

                            st.rerun()


def show_chat_interface(user_id: int):
    """Show chat interface with Carely"""
    user = UserCRUD.get_user(user_id)

    # Complete CSS rewrite for new chat UI design with AGGRESSIVE whitespace reduction
    st.markdown("""
        <style>
/* ============================================ */
/* ULTRA AGGRESSIVE WHITESPACE REDUCTION */
/* ============================================ */
/* Hide Streamlit header completely */
header, [data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
}

.stApp {
    background: linear-gradient(180deg, #F4F7FF 0%, #FFFFFF 60%) !important;
}
 
/* Remove ALL top padding/margin from containers */
.main .block-container,
div.block-container,
section.main > div.block-container {
    padding-top: 0.3rem !important;
    margin-top: 0 !important;
    padding-bottom: 0.5rem !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stAppViewContainer"] > section {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Remove first element top margin */
.block-container > div:first-child,
.element-container:first-child,
[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Reduce vertical block gaps */
[data-testid="stVerticalBlock"] {
    gap: 0.2rem !important;
}
 
/* ============================================ */
/* CHAT HEADER - COMPACT */
/* ============================================ */
.chat-header {
    background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 40%, #9FA8FF 100%);
    color: #111827;
    border-radius: 20px;
    padding: 12px 24px;
    max-width: 800px;
    margin: 0 auto 10px auto !important;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}
 
.chat-header-title {
    font-family: "Inter", sans-serif;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 2px;
}
 
.chat-header-subtitle {
    font-size: 14px;
    font-weight: 400;
    font-family: "Inter", sans-serif;
}
 
/* ============================================ */
/* CHAT MESSAGES CONTAINER - COMPACT */
/* ============================================ */
.chat-messages-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 12px;
}

.chat-container {
    padding: 4px 0 !important;
    margin: 0 !important;
}
 
/* Hide default Streamlit chat messages */
[data-testid="stChatMessage"] {
    display: none !important;
}

/* ============================================ */
/* GLOBAL COMPACT SPACING FOR CHAT */
/* ============================================ */
/* Remove all default Streamlit vertical spacing in chat area */
.chat-container div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

.chat-container div[data-testid="element-container"] {
    margin: 0 !important;
    padding: 0 !important;
}

.chat-container div[data-testid="stHorizontalBlock"] {
    gap: 4px !important;
    margin-bottom: 6px !important;
}

/* Remove spacing from markdown elements in chat */
.chat-container .stMarkdown {
    margin: 0 !important;
    padding: 0 !important;
}

.chat-container .stMarkdown p {
    margin: 0 !important;
    padding: 0 !important;
}
 
/* ============================================ */
/* MESSAGE ROWS - TIGHT SPACING */
/* ============================================ */
.chat-row {
    display: flex;
    flex-direction: row;
    margin-bottom: 6px !important;
    margin-top: 0 !important;
    align-items: flex-start;
    gap: 6px;
    width: 100%;
    padding: 0 !important;
}
 
/* Bot messages - left aligned */
.chat-row.bot {
    justify-content: flex-start;
}
 
/* User messages - right aligned */
.chat-row.user {
    justify-content: flex-end;
}

/* Bubble wrapper for user messages */
.bubble-wrapper {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    gap: 4px;
    max-width: 80%;
}

/* Bubble content wrapper */
.bubble-content {
    display: flex;
    flex-direction: column;
    max-width: 100%;
}

/* ============================================ */
/* AI MESSAGE ROW - STREAMLIT COLUMNS LAYOUT */
/* ============================================ */
/* Bot avatar column styling - using image */
.bot-avatar-col,
div[data-testid="column"]:first-child div[data-testid="stImage"] {
    width: 48px !important;
    height: 48px !important;
    min-width: 48px !important;
    min-height: 48px !important;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 0 !important;
    margin: 0 !important;
}

/* Style the AI avatar image - high quality rendering */
div[data-testid="stImage"] img {
    width: 48px !important;
    height: 48px !important;
    border-radius: 0 !important;
    object-fit: contain !important;
    image-rendering: -webkit-optimize-contrast !important;
    image-rendering: crisp-edges !important;
}

/* Remove extra padding from image container in chat - AVATAR STYLING */
.chat-container div[data-testid="stImage"],
div[data-testid="column"] div[data-testid="stImage"] {
    margin: 0 !important;
    padding: 0 !important;
}

/* Style the AI avatar image element - preserve original design */
div[data-testid="column"]:first-child img,
.chat-container img {
    width: 48px !important;
    height: 48px !important;
    min-width: 48px !important;
    min-height: 48px !important;
    max-width: 48px !important;
    max-height: 48px !important;
    border-radius: 0 !important;
    object-fit: contain !important;
    image-rendering: -webkit-optimize-contrast !important;
    image-rendering: crisp-edges !important;
}

/* Hide any extra elements in the avatar column */
div[data-testid="column"]:first-child div[data-testid="stImage"] ~ *,
div[data-testid="column"]:first-child > div > div:not([data-testid="stImage"]) {
    display: none !important;
}

/* Bot bubble column styling */
.bot-bubble-col {
    display: flex;
    flex-direction: column;
    max-width: 100%;
    margin: 0 !important;
    padding: 0 !important;
}

/* Listen button wrapper - compact */
.listen-btn-wrapper {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    min-height: 36px;
    padding-top: 4px;
    margin: 0 !important;
}

/* Style the listen button inside the wrapper */
.listen-btn-wrapper button,
.listen-btn-wrapper .stButton button {
    min-height: 36px !important;
    height: 36px !important;
    width: 36px !important;
    min-width: 36px !important;
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 50% !important;
    font-size: 18px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 40%, #9FA8FF 100%) !important;
    border: none !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.10) !important;
    cursor: pointer !important;
}

.listen-btn-wrapper button:hover,
.listen-btn-wrapper .stButton button:hover {
    transform: scale(1.08) !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15) !important;
}

/* Align columns vertically in AI message rows */
div[data-testid="column"]:has(.bot-avatar-col),
div[data-testid="column"]:has(.bot-bubble-col),
div[data-testid="column"]:has(.listen-btn-wrapper) {
    display: flex !important;
    align-items: flex-start !important;
    padding: 0 !important;
    margin: 0 !important;
}
 
/* ============================================ */
/* AVATARS - COMPACT */
/* ============================================ */
.chat-avatar,
.avatar,
.avatar-bot,
.avatar-user,
div.avatar,
div.avatar-bot,
div.avatar-user,
.chat-row .avatar,
.chat-row.bot .avatar,
.chat-row.user .avatar {
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    color: white !important;
    flex-shrink: 0 !important;
    margin-top: 0 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.12) !important;
    aspect-ratio: 1 / 1 !important;
}

.avatar-bot,
div.avatar-bot,
.chat-row.bot .avatar,
.chat-row.bot .avatar-bot {
    background: radial-gradient(circle at 30% 20%, #FDE68A, #6366F1) !important;
    margin-right: 6px !important;
    margin-left: 0 !important;
    margin-top: 0 !important;
    flex-shrink: 0 !important;
}

.avatar-user,
div.avatar-user,
.chat-row.user .avatar,
.chat-row.user .avatar-user {
    background: radial-gradient(circle at 30% 20%, #F97316, #F97373) !important;
    margin-left: 6px !important;
    margin-right: 0 !important;
    margin-top: 0 !important;
    flex-shrink: 0 !important;
}

/* User bubble wrapper alignment */
.user-bubble-wrapper {
    justify-content: flex-end !important;
}

/* Target Streamlit's default avatar elements */
[data-testid="stChatMessage"] [data-baseweb="avatar"],
[data-testid="stChatMessage"] img[alt*="avatar"],
[data-testid="stChatMessage"] img {
    width: 56px !important;
    height: 56px !important;
    min-width: 56px !important;
    min-height: 56px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
}

/* Hide Streamlit's default small avatars and replace with our styled ones */
[data-testid="stChatMessage"] [data-baseweb="avatar"] {
    display: none !important;
}
 
/* ============================================ */
/* CHAT BUBBLES */
/* ============================================ */
.chat-bubble {
    display: inline-block;
    width: fit-content;
    max-width: 100%;
    padding: 12px 18px;
    border-radius: 20px;
    font-family: "Inter", sans-serif;
    font-size: 15px;
    line-height: 1.5;
    word-wrap: break-word;
    position: relative;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
 
.chat-bubble-bot {
    background: #E0E7FF;
    color: #111827;
    border: 1px solid #C7D2FE;
    border-top-left-radius: 4px; /* Make it look like a speech bubble */
}
 
.chat-bubble-user {
    background: #FFE8F6;
    color: #1A1A1A;
    border: 1px solid #FFB3D9;
    border-top-right-radius: 4px; /* Make it look like a speech bubble */
}
 
/* ============================================ */
/* TIMESTAMPS */
/* ============================================ */
.chat-timestamp {
    font-size: 11px;
    color: #95A5A6;
    margin-top: 2px;
    margin-bottom: 0;
    padding: 0;
    font-family: "Inter", sans-serif;
    display: block;
    line-height: 1.2;
}
 
.chat-bubble-bot + .chat-timestamp,
.bubble-content .chat-timestamp {
    text-align: left;
    padding-left: 4px;
}
 
.chat-bubble-user + .chat-timestamp,
.user-bubble-wrapper .chat-timestamp {
    text-align: right;
    padding-right: 4px;
}
 
/* ============================================ */
/* MESSAGE CONTENT SPECIFIC STYLES */
/* ============================================ */
.chat-bubble p {
    margin: 0;
    padding: 0;
}
 
.chat-bubble strong {
    color: #111827;
}
 
/* ============================================ */
/* QUICK ACTIONS / BUTTONS */
/* ============================================ */
.quick-actions {
    display: flex;
    gap: 8px;
    margin-top: 16px;
    flex-wrap: wrap;
    justify-content: center;
}
 
.quick-action-btn {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 8px 16px;
    font-family: "Inter", sans-serif;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
}
 
.quick-action-btn:hover {
    background: #F3F4F6;
    transform: translateY(-1px);
}
 
/* ============================================ */
/* INPUT AREA */
/* ============================================ */
.chat-input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 16px;
    border-top: 1px solid #E5E7EB;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}
 
/* ============================================ */
/* SIDEBAR LOGO AND STYLING */
/* ============================================ */
[data-testid="stSidebar"] {
    min-width: 280px !important;
    width: 280px !important;
}

[data-testid="stSidebar"] [data-testid="stImage"] {
    width: 100% !important;
    max-width: 280px !important;
    padding: 0 1rem !important;
    margin-bottom: 1rem !important;
}

[data-testid="stSidebar"] [data-testid="stImage"] img {
    width: 100% !important;
    height: auto !important;
    object-fit: contain !important;
}

/* ============================================ */
/* LOGOUT BUTTON IN SIDEBAR */
/* ============================================ */
div[data-testid="stSidebar"] button[kind="secondary"] {
    background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 40%, #9FA8FF 100%) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}
 
/* Responsive adjustments */
@media (max-width: 768px) {
    .chat-bubble {
        max-width: 85%;
    }
    .chat-avatar {
        width: 36px;
        height: 36px;
        font-size: 18px;
    }
    .chat-header {
        margin: 0 16px 16px 16px !important;
        padding: 16px 24px;
    }
}
</style>
    """,
                unsafe_allow_html=True)

    # Vibrant header with new gradient
    st.markdown(f"""
        <div class="chat-header">
            <div class="chat-header-title">Chat with Carely</div>
            <div class="chat-header-subtitle">Hello {user.name}! I'm here to help you today 🌟</div>
        </div>
    """,
                unsafe_allow_html=True)

    # Display emergency safety sheet if emergency detected
    if st.session_state.get("emergency_data") and not st.session_state.get(
            "emergency_handled"):
        emergency_data = st.session_state.emergency_data
        show_emergency_safety_sheet(
            user_id=user_id,
            concerns=emergency_data.get("concerns", []),
            severity=emergency_data.get("severity", "medium"),
            message=emergency_data.get("message", ""))

        if st.session_state.get("emergency_handled"):
            st.session_state.emergency_data = None
            st.rerun()

        return

    # Check if Memory Game should be shown
    if st.session_state.get("show_memory_game", False):
        show_memory_game()
        return

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Initialize pending_action for Quick Actions
    if 'pending_action' not in st.session_state:
        st.session_state.pending_action = None

    # Initialize flag for expecting medication name input
    if 'expecting_medication_name' not in st.session_state:
        st.session_state.expecting_medication_name = False

    # Initialize proactive greeting flag
    if 'proactive_greeting_sent' not in st.session_state:
        st.session_state.proactive_greeting_sent = False

    # Load recent conversations
    if not st.session_state.chat_history:
        recent_convs = ConversationCRUD.get_user_conversations(user_id,
                                                               limit=10)
        for conv in reversed(recent_convs):
            st.session_state.chat_history.append({
                "role": "user",
                "content": conv.message,
                "timestamp": conv.timestamp
            })
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": conv.response,
                "timestamp": conv.timestamp
            })

        # Send proactive greeting when chat opens
        # Show greeting if: no recent conversations OR last conversation was >4 hours ago
        should_greet = False
        if len(recent_convs) == 0:
            should_greet = True
        elif recent_convs[0].timestamp:
            from utils.timezone_utils import to_central
            last_conv_time = to_central(recent_convs[0].timestamp)
            time_since_last = (now_central() -
                               last_conv_time).total_seconds() / 3600  # hours
            if time_since_last > 4:  # More than 4 hours since last conversation
                should_greet = True

        if should_greet and not st.session_state.proactive_greeting_sent:
            try:
                proactive_message = st.session_state.companion_agent.generate_proactive_greeting(
                    user_id)
                if proactive_message:
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role":
                        "assistant",
                        "content":
                        proactive_message,
                        "timestamp":
                        now_central(),
                        "is_proactive":
                        True
                    })

                    # Save to database
                    ConversationCRUD.save_conversation(
                        user_id=user_id,
                        message="[Proactive Greeting]",
                        response=proactive_message,
                        conversation_type="proactive_greeting")

                    st.session_state.proactive_greeting_sent = True
            except Exception as e:
                # Silently fail if greeting generation fails
                pass

    # Check for pending reminders and display them proactively
    if 'reminders_displayed' not in st.session_state:
        st.session_state.reminders_displayed = set()

    pending_reminders = ReminderCRUD.get_pending_reminders(user_id)
    for reminder in pending_reminders:
        if reminder.id not in st.session_state.reminders_displayed:
            # Add reminder to chat as an assistant message
            reminder_content = reminder.message

            # Add quick action button for medication reminders
            quick_actions = []
            if reminder.reminder_type == "medication":
                quick_actions = ["log_medication"]

            st.session_state.chat_history.append({
                "role":
                "assistant",
                "content":
                reminder_content,
                "timestamp":
                reminder.scheduled_time,
                "quick_actions":
                quick_actions,
                "reminder_id":
                reminder.id,
                "medication_id":
                reminder.medication_id
            })

            st.session_state.reminders_displayed.add(reminder.id)

            # Mark reminder as displayed (completed)
            ReminderCRUD.complete_reminder(reminder.id)

    # Chat container - compact spacing
    st.markdown("""
        <div class="chat-container" style='padding: 4px 0; margin: 0;'>
    """,
                unsafe_allow_html=True)

    chat_container = st.container()

    # Initialize TTS state
    if 'playing_audio' not in st.session_state:
        st.session_state.playing_audio = None

    with chat_container:
        # Display chat history with new chat-row structure
        for idx, message in enumerate(
                st.session_state.chat_history[-20:]
        ):  # Show last 20 messages (10 exchanges)
            content = message["content"]

            # Escape HTML in content for safety
            escaped_content = html.escape(content)
            # Convert newlines to <br> for proper display
            formatted_content = escaped_content.replace('\n', '<br>')

            if message["role"] == "user":
                # User message - right aligned (avatar on extreme right, bubble just left of it)
                # Format timestamp
                timestamp_str = ""
                if message.get("timestamp"):
                    timestamp_str = f'<div class="chat-timestamp">{format_time_central(message["timestamp"], "%I:%M %p")}</div>'

                st.markdown(f"""
                    <div class="chat-row user">
                        <div class="bubble-wrapper user-bubble-wrapper">
                            <div class="bubble-content">
                                <div class="chat-bubble chat-bubble-user">{formatted_content}</div>
                                {timestamp_str}
                            </div>
                        </div>
                        <div class="avatar avatar-user">👤</div>
                    </div>
                """,
                            unsafe_allow_html=True)
            else:
                # AI message - use st.columns for proper layout: avatar | bubble | listen button
                # Extract video URL if present
                video_url = None
                display_content = content
                if "youtube.com/watch?v=" in content or "youtu.be/" in content:
                    lines = content.split("\n")
                    text_lines = []
                    for line in lines:
                        if "youtube.com/watch?v=" in line or "youtu.be/" in line:
                            video_url = line.strip()
                        else:
                            text_lines.append(line)
                    display_content = "\n".join(text_lines)

                # Format content for display
                text_content = html.escape(display_content).replace(
                    '\n', '<br>')
                timestamp_str = ""
                if message.get("timestamp"):
                    timestamp_str = f'<div class="chat-timestamp">{format_time_central(message["timestamp"], "%I:%M %p")}</div>'

                # Create three-column layout: avatar | bubble | listen button
                avatar_col, bubble_col, listen_col = st.columns([0.5, 8, 0.8],
                                                                gap="small")

                with avatar_col:
                    st.image("ai_avatar.png", width=48)

                with bubble_col:
                    st.markdown(f"""
                        <div class="bot-bubble-col">
                            <div class="chat-bubble chat-bubble-bot">{text_content}</div>
                            {timestamp_str}
                        </div>
                    """,
                                unsafe_allow_html=True)

                with listen_col:
                    # Listen button in rightmost column - vertically centered
                    st.markdown('<div class="listen-btn-wrapper">',
                                unsafe_allow_html=True)
                    if st.button("🔊",
                                 key=f"listen_{idx}",
                                 help="Listen to this message"):
                        st.session_state.playing_audio = idx
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                # Play audio if this message is selected
                if st.session_state.playing_audio == idx:
                    audio_bytes = generate_speech_audio(content, slow=True)
                    if audio_bytes:
                        st.audio(audio_bytes,
                                 format='audio/mp3',
                                 autoplay=True)
                        st.session_state.playing_audio = None

                # Embed YouTube video below if present
                if video_url:
                    st.video(video_url)

    # Close chat panel container
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle quick action button clicks
    if st.session_state.get("pending_action"):
        action = st.session_state.pending_action
        st.session_state.pending_action = None

        if action == "log_medication":
            # Get user's medications to let them choose
            medications = MedicationCRUD.get_user_medications(user_id,
                                                              active_only=True)

            if medications:
                # Show medication selection prompt
                med_list = ", ".join([med.name for med in medications])
                response_text = f"Please specify which medication you took. Your medications include: {med_list}"

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": now_central(),
                    "quick_actions": []
                })

                # Set flag to expect medication name in next input
                st.session_state.expecting_medication_name = True
            else:
                response_text = "I don't see any medications in your schedule. Would you like to add one?"
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": now_central(),
                    "quick_actions": []
                })

            st.rerun()

        elif action == "play_music":
            music_data = st.session_state.companion_agent.handle_play_music()
            st.session_state.chat_history.append({
                "role":
                "assistant",
                "content":
                music_data["message"],
                "timestamp":
                now_central(),
                "quick_actions": ["fun_corner", "memory_cue"]
            })
            st.rerun()

        elif action == "fun_corner":
            joke_or_puzzle = st.session_state.companion_agent.handle_fun_corner(
                "joke")
            message_text = f"Here's a joke for you! 😊\n\n{joke_or_puzzle}"
            st.session_state.chat_history.append({
                "role":
                "assistant",
                "content":
                message_text,
                "timestamp":
                now_central(),
                "quick_actions": ["play_music", "memory_cue"]
            })
            st.rerun()

        elif action == "memory_cue":
            memory_question = st.session_state.companion_agent.generate_memory_cue(
                user_id)
            st.session_state.chat_history.append({
                "role":
                "assistant",
                "content":
                memory_question,
                "timestamp":
                now_central(),
                "quick_actions": ["fun_corner", "play_music"]
            })
            st.rerun()

    # Integrated input bar with voice and text - ULTRA COMPACT spacing
    st.markdown(
        "<hr style='margin: 2px 0; border: none; border-top: 1px solid #eee;'>",
        unsafe_allow_html=True)
    st.markdown(
        "<p class='input-label' style='font-size: 0.85rem; font-weight: 600; margin: 0 0 2px 0; padding: 0;'>Type or speak your message:</p>",
        unsafe_allow_html=True)

    # Add CSS to align all input elements properly and style buttons - ULTRA COMPACT
    st.markdown("""
        <style>
        /* ============================================ */
        /* ULTRA COMPACT INPUT SECTION */
        /* ============================================ */
        /* Align all input row elements on same baseline */
        div[data-testid="column"] {
            display: flex !important;
            align-items: flex-end !important;
        }
        
        /* Ensure text input aligns with buttons */
        div[data-testid="stTextInput"] {
            margin-bottom: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Remove all spacing from input label */
        .input-label {
            margin: 0 0 2px 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
        }
        
        /* ============================================ */
        /* MIC COLUMN - INLINE WITH TEXT INPUT          */
        /* ============================================ */

        /* Third column in the input row = mic column */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Pink pill container behind the mic component */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3)
            > div[data-testid="stVerticalBlock"] {
            background: linear-gradient(135deg, #FFE8F6 0%, #FFD6EC 100%) !important;
            border-radius: 10px !important;
            padding: 2px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06) !important;
            width: 100% !important;
            min-height: 42px !important;
            height: 42px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* Make sure the mic recorder fits nicely */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) iframe {
            max-height: 36px !important;
            border-radius: 8px !important;
        }

        /* ============================================ */
        /* STYLE MIC ICON TO MATCH PINK THEME           */
        /* ============================================ */

        /* Target the mic recorder iframe wrapper */
        iframe[title="speech_to_text"] {
            background: linear-gradient(135deg, #FFE8F6 0%, #FFD6EC 100%) !important;
            border-radius: 10px !important;
            border: none !important;
        }

        /* Override internal background + icon colors */
        iframe[title="speech_to_text"] * {
            background: transparent !important;
            color: #7A3F6C !important; /* Deep mauve */
        }

        /* Style the mic SVG icon */
        iframe[title="speech_to_text"] svg {
            fill: #7A3F6C !important;
            stroke: #7A3F6C !important;
        }

        /* Hover effect like Send button */
        iframe[title="speech_to_text"]:hover {
            filter: brightness(1.1);
            transform: translateY(-1px);
            transition: all 0.15s ease-in-out;
        }

 
        
        /* Ensure send button aligns */
        div[data-testid="column"] > div > div > button {
            margin-bottom: 0 !important;
        }
        
        /* Remove ALL spacing from horizontal blocks in input area */
        div[data-testid="stHorizontalBlock"] {
            gap: 4px !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Compact quick actions section */
        .section-header {
            margin: 4px 0 2px 0 !important;
            padding: 0 !important;
        }
        
        /* Make quick action buttons smaller */
        .stButton button[kind="secondary"] {
            padding: 4px 6px !important;
            font-size: 12px !important;
            min-height: 36px !important;
        }
        
        /* Reduce text input height */
        .stTextInput input {
            height: 42px !important;
            min-height: 42px !important;
            padding: 0.5rem 1rem !important;
        }
        
        /* Reduce send button size */
        button[kind="primary"],
        .stButton button[kind="primary"] {
            height: 42px !important;
            min-height: 42px !important;
            padding: 0 0.8rem !important;
        }

        </style>
        <script>
        // Function to force user chat bubbles and avatars to extreme right
        function forceUserChatToRight() {
            const userChatRows = document.querySelectorAll('.chat-row.user');
            
            userChatRows.forEach(chatRow => {
                // Find the avatar
                const avatar = chatRow.querySelector('.avatar-user');
                if (!avatar) return;
                
                // Find element container
                const elementContainer = chatRow.closest('div[data-testid="element-container"]');
                if (elementContainer) {
                    // Extend to right edge
                    elementContainer.style.marginRight = '-8px';
                    elementContainer.style.paddingRight = '0';
                    elementContainer.style.width = 'calc(100% + 8px)';
                }
                
                // Force avatar to extreme right
                avatar.style.marginRight = '0';
                avatar.style.paddingRight = '0';
                
                // Force chat row to right
                chatRow.style.marginRight = '0';
                chatRow.style.paddingRight = '0';
            });
        }
        
        // Run user chat alignment
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', forceUserChatToRight);
        } else {
            forceUserChatToRight();
        }
        
        setTimeout(forceUserChatToRight, 100);
        setTimeout(forceUserChatToRight, 500);
        setTimeout(forceUserChatToRight, 1000);
        
        // Monitor for new messages
        const userChatObserver = new MutationObserver(function(mutations) {
            forceUserChatToRight();
            enlargeAvatars();
        });
        userChatObserver.observe(document.body, { childList: true, subtree: true });
        
        // Function to style avatars with compact sizing
        function enlargeAvatars() {
            // Target custom HTML avatars - use compact 40px size
            const customAvatars = document.querySelectorAll('.avatar, .avatar-bot, .avatar-user, .chat-avatar');
            customAvatars.forEach(avatar => {
                avatar.style.width = '40px';
                avatar.style.height = '40px';
                avatar.style.minWidth = '40px';
                avatar.style.minHeight = '40px';
                avatar.style.borderRadius = '50%';
                avatar.style.fontSize = '20px';
                avatar.style.display = 'flex';
                avatar.style.alignItems = 'center';
                avatar.style.justifyContent = 'center';
                avatar.style.flexShrink = '0';
                avatar.style.marginTop = '0';
                avatar.style.boxShadow = '0 2px 4px rgba(0,0,0,0.12)';
                
                // Apply gradient backgrounds
                if (avatar.classList.contains('avatar-bot') || avatar.classList.contains('bot')) {
                    avatar.style.background = 'radial-gradient(circle at 30% 20%, #FDE68A, #6366F1)';
                    avatar.style.marginRight = '6px';
                    avatar.style.marginLeft = '0';
                } else if (avatar.classList.contains('avatar-user') || avatar.classList.contains('user')) {
                    avatar.style.background = 'radial-gradient(circle at 30% 20%, #F97316, #F97373)';
                    avatar.style.marginLeft = '6px';
                    avatar.style.marginRight = '0';
                }
            });
            
            // Target Streamlit's chat message avatars
            const streamlitMessages = document.querySelectorAll('[data-testid="stChatMessage"]');
            streamlitMessages.forEach(msg => {
                const isUser = msg.getAttribute('aria-label')?.includes('user');
                const defaultAvatar = msg.querySelector('[data-baseweb="avatar"]');
                
                // Hide Streamlit's default avatar
                if (defaultAvatar) {
                    defaultAvatar.style.display = 'none';
                }
                
                // Create or find our custom avatar
                let customAvatar = msg.querySelector('.avatar, .avatar-bot, .avatar-user');
                if (!customAvatar) {
                    customAvatar = document.createElement('div');
                    customAvatar.className = isUser ? 'avatar avatar-user' : 'avatar avatar-bot';
                    customAvatar.textContent = isUser ? '👤' : '👾';
                    customAvatar.style.cssText = 'width: 40px !important; height: 40px !important; border-radius: 50% !important; display: flex !important; align-items: center !important; justify-content: center !important; font-size: 20px !important; font-weight: 700 !important; color: white !important; flex-shrink: 0 !important; margin-top: 0 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.12) !important;';
                    customAvatar.style.background = isUser ? 'radial-gradient(circle at 30% 20%, #F97316, #F97373) !important' : 'radial-gradient(circle at 30% 20%, #FDE68A, #6366F1) !important';
                    if (isUser) {
                        customAvatar.style.marginLeft = '6px';
                        customAvatar.style.marginRight = '0';
                    } else {
                        customAvatar.style.marginRight = '6px';
                        customAvatar.style.marginLeft = '0';
                    }
                    msg.insertBefore(customAvatar, msg.firstChild);
                } else {
                    // Ensure existing custom avatar is compact
                    customAvatar.style.width = '40px';
                    customAvatar.style.height = '40px';
                    customAvatar.style.fontSize = '20px';
                }
            });
        }
        
        // Run immediately
        enlargeAvatars();
        
        // Run on load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', enlargeAvatars);
        } else {
            enlargeAvatars();
        }
        
        // Run after delays
        setTimeout(enlargeAvatars, 100);
        setTimeout(enlargeAvatars, 500);
        setTimeout(enlargeAvatars, 1000);
        setTimeout(enlargeAvatars, 2000);
        </script>
    """,
                unsafe_allow_html=True)

    # Additional CSS for Quick Action buttons
    st.markdown("""
        <style>
        /* Style Quick Action buttons with Carely gradient (matching Chat with Carely header) */
        button[kind="secondary"],
        .stButton button[kind="secondary"],
        .stButton button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 40%, #9FA8FF 100%) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 18px !important;
            font-family: "Inter", sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.07) !important;
            transition: all 0.3s ease !important;
        }
        
        /* Ensure Quick Action button text and emojis are black and bold */
        button[kind="secondary"] *,
        .stButton button[kind="secondary"] *,
        .stButton button[data-testid="baseButton-secondary"] * {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        
        button[kind="secondary"]:hover,
        .stButton button[kind="secondary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 14px rgba(0,0,0,0.10) !important;
        }
        
        button[kind="secondary"]:active,
        .stButton button[kind="secondary"]:active {
            transform: translateY(0px) !important;
        }
        </style>
    """,
                unsafe_allow_html=True)

    # Create columns for text input, send button, and mic button side by side
    text_col, send_col, mic_col = st.columns([8, 1, 1], gap="small")

    prompt = None
    is_voice = False

    with text_col:
        # Initialize or get the current input value
        if f'clear_input_{user_id}' in st.session_state and st.session_state[
                f'clear_input_{user_id}']:
            st.session_state[f'chat_text_{user_id}'] = ""
            st.session_state[f'clear_input_{user_id}'] = False

        # Text input
        text_input = st.text_input(
            "Message",
            placeholder=f"Type your message here, {user.name}...",
            key=f"chat_text_{user_id}",
            label_visibility="collapsed")

    with send_col:
        # Send button
        send_clicked = st.button("➤",
                                 key=f"send_btn_{user_id}",
                                 use_container_width=True,
                                 type="primary")

    with mic_col:
        # Render mic recorder directly; styling handled via CSS on the mic column
        voice_text = speech_to_text(
            language='en',
            start_prompt="🎤",
            stop_prompt="⏹️",
            just_once=True,
            use_container_width=True,
            key=f'voice_input_{user_id}',
        )

    # Persistent Quick Actions - compact spacing
    st.markdown(
        "<p class='section-header' style='font-weight: 600; margin: 6px 0 4px 0; font-size: 0.95rem;'>Quick Actions:</p>",
        unsafe_allow_html=True)

    # Use equal columns with proper button sizing
    action_col1, action_col2, action_col3, action_col4, action_col5 = st.columns(
        5, gap="small")

    with action_col1:
        if st.button("🕐 Log\nMedication",
                     key="persistent_log_med",
                     use_container_width=True):
            st.session_state.pending_action = "log_medication"
            st.rerun()

    with action_col2:
        if st.button("🎵 Play\nMusic",
                     key="persistent_play_music",
                     use_container_width=True):
            st.session_state.pending_action = "play_music"
            st.rerun()

    with action_col3:
        if st.button("🧩 Fun\nCorner",
                     key="persistent_fun_corner",
                     use_container_width=True):
            st.session_state.pending_action = "fun_corner"
            st.rerun()

    with action_col4:
        if st.button("🧠 Memory\nCue",
                     key="persistent_memory_cue",
                     use_container_width=True):
            st.session_state.pending_action = "memory_cue"
            st.rerun()

    with action_col5:
        if st.button("🎮 Memory\nGame",
                     key="persistent_memory_game",
                     use_container_width=True):
            st.session_state.show_memory_game = True
            st.rerun()

    # Handle Enter key press using session state
    if text_input and text_input != st.session_state.get(
            f'last_input_{user_id}', ''):
        prompt = text_input
        is_voice = False
        st.session_state[f'last_input_{user_id}'] = text_input
    # Process voice input immediately when received
    elif voice_text:
        prompt = voice_text
        is_voice = True
    elif send_clicked and text_input:
        prompt = text_input
        is_voice = False

    # Process input (from either voice or text)
    if prompt:
        # Add user message to chat (with mic emoji for voice input)
        display_message = f"🎙️ {prompt}" if is_voice else prompt

        with st.chat_message("user"):
            st.write(display_message)

        # Check if we're expecting a medication name (from "Log Medication" button)
        if st.session_state.get("expecting_medication_name", False):
            st.session_state.expecting_medication_name = False

            # Try to find the medication by name
            medications = MedicationCRUD.get_user_medications(user_id,
                                                              active_only=True)
            medication_id = None
            medication_name = None

            # Case-insensitive search
            prompt_lower = prompt.lower().strip()
            for med in medications:
                if prompt_lower in med.name.lower() or med.name.lower(
                ) in prompt_lower:
                    medication_id = med.id
                    medication_name = med.name
                    break

            # Generate response
            with st.chat_message("assistant", avatar="👾"):
                if medication_id:
                    # Log the medication
                    with st.spinner("Logging your medication..."):
                        log_result = st.session_state.companion_agent.log_medication_tool(
                            user_id=user_id, medication_id=medication_id)

                    st.write(log_result)
                    response_text = log_result
                else:
                    # Medication not found
                    med_list = ", ".join([med.name for med in medications[:5]])
                    response_text = f"I couldn't find '{prompt}' in your medication list. Your medications are: {med_list}. Could you try again?"
                    st.write(response_text)
                    st.session_state.expecting_medication_name = True  # Ask again

            # Update chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": display_message,
                "timestamp": now_central()
            })
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": now_central(),
                "quick_actions": []
            })
        else:
            # Normal conversation flow
            # Generate AI response
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Carely is thinking..."):
                    response_data = st.session_state.companion_agent.generate_response(
                        user_id=user_id, user_message=prompt)

                st.write(response_data["response"])

                st.write(response_data["response"])

                # Show sentiment if available
                if response_data.get("sentiment_score") is not None:
                    sentiment_emoji = get_sentiment_emoji(
                        response_data["sentiment_score"])
                    st.caption(
                        f"Detected mood: {sentiment_emoji} {response_data['sentiment_label']}"
                    )

            # Update session state for normal conversation
            st.session_state.chat_history.append({
                "role": "user",
                "content": display_message,
                "timestamp": now_central()
            })
            st.session_state.chat_history.append({
                "role":
                "assistant",
                "content":
                response_data["response"],
                "timestamp":
                now_central(),
                "quick_actions":
                response_data.get("quick_actions", [])
            })

            # Check for emergency
            if response_data.get("is_emergency") and not st.session_state.get(
                    "emergency_handled"):
                st.session_state.emergency_data = {
                    "concerns": response_data.get("emergency_concerns", []),
                    "severity": response_data.get("emergency_severity",
                                                  "medium"),
                    "message": prompt
                }

        # Clear the input field after sending
        st.session_state[f'clear_input_{user_id}'] = True

        # Rerun to show the new messages
        st.rerun()

    # Mood analysis (removed quick action buttons)
    if st.session_state.get('show_mood_analysis', False):
        st.subheader("📈 Conversation Mood Analysis")

        conversations = ConversationCRUD.get_recent_sentiment_data(user_id,
                                                                   days=7)
        if conversations:
            # Create sentiment chart
            df = pd.DataFrame([{
                "timestamp": conv.timestamp,
                "sentiment_score": conv.sentiment_score,
                "sentiment_label": conv.sentiment_label
            } for conv in conversations if conv.sentiment_score is not None])

            fig = px.line(df,
                          x="timestamp",
                          y="sentiment_score",
                          title="Mood Trends Over Time",
                          color_discrete_sequence=["#1f77b4"])
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.update_layout(yaxis_title="Mood Score",
                              xaxis_title="Time",
                              yaxis_range=[-1, 1])

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No mood data available yet. Keep chatting with Carely!")


def show_medication_management(user_id: int):
    """Show medication management interface"""
    user = UserCRUD.get_user(user_id)
    st.markdown(
        f"<h1 style='margin: 0 0 0.5rem 0; color: #E74C3C; font-size: 1.8rem; font-weight: 700;'>💊 Medication Management - {user.name}</h1>",
        unsafe_allow_html=True)

    # Medication overview
    medications = MedicationCRUD.get_user_medications(user_id)

    if medications:
        st.markdown(
            "<h3 style='margin: 0.5rem 0 0.4rem 0; color: #3498db; font-size: 1.3rem;'>Current Medications</h3>",
            unsafe_allow_html=True)

        # Add CSS for clickable medication items and compact layout
        st.markdown("""
            <style>
            /* Style medication expanders to look more clickable */
            div[data-testid="stExpander"] {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                margin-bottom: 8px;
                background-color: white;
                transition: all 0.3s ease;
            }
            
            div[data-testid="stExpander"]:hover {
                border-color: #3498db;
                box-shadow: 0 4px 8px rgba(52, 152, 219, 0.2);
                transform: translateY(-2px);
            }
            
            /* Style the expander summary (header) */
            div[data-testid="stExpander"] summary {
                cursor: pointer;
                padding: 10px;
                font-weight: 600;
                color: #2c3e50;
            }
            
            div[data-testid="stExpander"] summary:hover {
                color: #3498db;
            }
            </style>
        """,
                    unsafe_allow_html=True)

        for med in medications:
            with st.expander(f"{med.name} - {med.dosage}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Frequency:** {med.frequency}")
                    if med.schedule_times:
                        times = json.loads(med.schedule_times)
                        st.write(f"**Times:** {', '.join(times)}")
                    if med.instructions:
                        st.write(f"**Instructions:** {med.instructions}")
                    st.write(f"**Active:** {'Yes' if med.active else 'No'}")

                with col2:
                    # Recent logs for this medication
                    adherence = MedicationLogCRUD.get_medication_adherence(
                        user_id, days=7)
                    med_logs = [
                        log for log in adherence.get("logs", [])
                        if log.medication_id == med.id
                    ]

                    if med_logs:
                        st.write("**Recent Activity:**")
                        for log in med_logs[-3:]:  # Last 3 logs
                            status_emoji = "✅" if log.status == "taken" else "❌" if log.status == "missed" else "⏸️"
                            st.write(
                                f"{status_emoji} {format_time_central(log.scheduled_time, '%m/%d %I:%M %p')} - {log.status}"
                            )

                    # Quick log button
                    if st.button(f"Log {med.name} as Taken",
                                 key=f"log_{med.id}"):
                        MedicationLogCRUD.log_medication_taken(
                            user_id=user_id,
                            medication_id=med.id,
                            scheduled_time=now_central(),
                            status="taken")
                        st.success(f"{med.name} logged as taken!")
                        st.rerun()

    else:
        st.info("No medications found. Add medications below.")

    # Medication adherence chart - compact spacing
    st.markdown(
        "<h3 style='margin: 0.8rem 0 0.4rem 0; color: #27AE60; font-size: 1.3rem;'>📊 Adherence Overview</h3>",
        unsafe_allow_html=True)

    # Time period selector
    period = st.selectbox("Select period:", ["Last 7 days", "Last 30 days"],
                          key="adherence_period")
    days = 7 if period == "Last 7 days" else 30

    adherence = MedicationLogCRUD.get_medication_adherence(user_id, days=days)

    # Custom metrics with BLACK text - using HTML instead of st.metric
    total_doses = adherence.get("total", 0)
    doses_taken = adherence.get("taken", 0)
    adherence_rate = adherence.get('adherence_rate', 0)

    st.markdown(f"""
        <div style='display: flex; gap: 1rem; margin: 0.5rem 0;'>
            <div style='flex: 1; background: white; padding: 0.8rem 1rem; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); text-align: center;'>
                <div style='font-size: 0.9rem; font-weight: 600; color: #000000; margin-bottom: 0.3rem;'>Total Doses</div>
                <div style='font-size: 1.8rem; font-weight: 700; color: #000000;'>{total_doses}</div>
            </div>
            <div style='flex: 1; background: white; padding: 0.8rem 1rem; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); text-align: center;'>
                <div style='font-size: 0.9rem; font-weight: 600; color: #000000; margin-bottom: 0.3rem;'>Doses Taken</div>
                <div style='font-size: 1.8rem; font-weight: 700; color: #000000;'>{doses_taken}</div>
            </div>
            <div style='flex: 1; background: white; padding: 0.8rem 1rem; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); text-align: center;'>
                <div style='font-size: 0.9rem; font-weight: 600; color: #000000; margin-bottom: 0.3rem;'>Adherence Rate</div>
                <div style='font-size: 1.8rem; font-weight: 700; color: #000000;'>{adherence_rate:.1f}%</div>
            </div>
        </div>
    """,
                unsafe_allow_html=True)

    # Adherence chart
    if adherence.get("logs"):
        df = pd.DataFrame([{
            "date":
            log.scheduled_time.date(),
            "status":
            log.status,
            "medication":
            next((med.name
                  for med in medications if med.id == log.medication_id),
                 "Unknown")
        } for log in adherence["logs"]])

        # Group by date and calculate daily adherence
        daily_adherence = df.groupby("date").apply(
            lambda x: (x["status"] == "taken").sum() / len(x) * 100,
            include_groups=False).reset_index(name="adherence_rate")

        # Convert to datetime and format as date string for clean x-axis display
        daily_adherence["date"] = pd.to_datetime(daily_adherence["date"])
        daily_adherence["date_str"] = daily_adherence["date"].dt.strftime(
            '%b %d')

        # Create line chart using date strings for clean x-axis
        fig = px.line(daily_adherence,
                      x="date_str",
                      y="adherence_rate",
                      title=f"Daily Adherence Rate ({period})",
                      range_y=[0, 105],
                      markers=True)

        # Style the line - sky blue (#87CEEB) line with white background
        fig.update_traces(line=dict(color='#87CEEB', width=3),
                          marker=dict(size=10,
                                      color='#87CEEB',
                                      line=dict(width=2, color='white')),
                          mode='lines+markers')

        # Add target line with annotation inside the chart area
        fig.add_hline(y=80,
                      line_dash="dash",
                      line_color="#27AE60",
                      annotation_text="Target: 80%",
                      annotation_position="bottom left",
                      annotation_font=dict(color="#27AE60", size=11))

        # White background layout with black axis labels
        fig.update_layout(yaxis_title="Adherence Rate (%)",
                          xaxis_title="Date",
                          showlegend=False,
                          hovermode='x unified',
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          font=dict(color='#000000'),
                          title_font=dict(color='#000000'),
                          margin=dict(t=40, b=50, l=60, r=20),
                          xaxis=dict(type='category'))

        fig.update_xaxes(showgrid=True,
                         gridcolor='#E0E0E0',
                         linecolor='#CCCCCC',
                         tickfont=dict(color='#000000'),
                         title_font=dict(color='#000000'))
        fig.update_yaxes(showgrid=True,
                         gridcolor='#E0E0E0',
                         linecolor='#CCCCCC',
                         tickfont=dict(color='#000000'),
                         title_font=dict(color='#000000'))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "No adherence data available yet. Start logging your medications to see trends!"
        )

    # Add new medication - compact spacing
    st.markdown(
        "<h3 style='margin: 0.8rem 0 0.4rem 0; color: #9B59B6; font-size: 1.3rem;'>➕ Add New Medication</h3>",
        unsafe_allow_html=True)

    # CSS for white button text - override Streamlit defaults
    st.markdown("""
        <style>
        button[kind="formSubmit"] {
            color: white !important;
            font-weight: 600 !important;
        }
        button[kind="formSubmit"] p {
            color: white !important;
        }
        button[kind="formSubmit"] span {
            color: white !important;
        }
        div[data-testid="stForm"] button {
            color: white !important;
        }
        div[data-testid="stForm"] button p {
            color: white !important;
        }
        </style>
    """,
                unsafe_allow_html=True)

    with st.form("add_medication"):
        col1, col2 = st.columns(2)

        with col1:
            med_name = st.text_input("Medication Name*")
            dosage = st.text_input("Dosage*",
                                   placeholder="e.g., 10mg, 1 tablet")
            frequency = st.selectbox("Frequency", [
                "daily", "twice_daily", "three_times_daily", "weekly",
                "as_needed"
            ])

        with col2:
            # Schedule times
            if frequency == "daily":
                times = [
                    st.time_input("Time", value=time(9, 0)).strftime("%H:%M")
                ]
            elif frequency == "twice_daily":
                time1 = st.time_input("Morning",
                                      value=time(9, 0)).strftime("%H:%M")
                time2 = st.time_input("Evening",
                                      value=time(21, 0)).strftime("%H:%M")
                times = [time1, time2]
            elif frequency == "three_times_daily":
                time1 = st.time_input("Morning",
                                      value=time(8, 0)).strftime("%H:%M")
                time2 = st.time_input("Afternoon",
                                      value=time(14, 0)).strftime("%H:%M")
                time3 = st.time_input("Evening",
                                      value=time(20, 0)).strftime("%H:%M")
                times = [time1, time2, time3]
            else:
                times = []

        instructions = st.text_area("Instructions (optional)",
                                    placeholder="Take with food, etc.")

        if st.form_submit_button("Add Medication"):
            if med_name and dosage:
                try:
                    MedicationCRUD.create_medication(user_id=user_id,
                                                     name=med_name,
                                                     dosage=dosage,
                                                     frequency=frequency,
                                                     schedule_times=times,
                                                     instructions=instructions
                                                     or None)
                    st.success(f"Added {med_name} successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding medication: {e}")
            else:
                st.error("Please fill in required fields (Name and Dosage)")


def show_health_insights(user_id: int):
    """Show health insights and analytics"""
    user = UserCRUD.get_user(user_id)
    
    st.markdown("""
        <style>
        /* Compact Health Insights page */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
        }
        
        /* Make metric labels black */
        [data-testid="stMetricLabel"] {
            color: #000000 !important;
        }
        [data-testid="stMetricLabel"] label,
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] div {
            color: #000000 !important;
        }
        
        /* Make metric values black */
        [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        [data-testid="stMetricValue"] div {
            color: #000000 !important;
        }
        
        /* Reduce vertical spacing */
        [data-testid="stVerticalBlock"] {
            gap: 0.3rem !important;
        }
        
        /* Compact subheaders */
        .stSubheader {
            margin-top: 0.3rem !important;
            margin-bottom: 0.2rem !important;
        }
        
        h2, h3 {
            margin-top: 0.3rem !important;
            margin-bottom: 0.2rem !important;
        }
        
        /* Compact divider */
        hr {
            margin: 0.3rem 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.header(f"📊 Health Insights - {user.name}")

    # Time period selector
    col1, col2 = st.columns([1, 3])
    with col1:
        period = st.selectbox("Time Period:", ["7 days", "30 days", "90 days"])
        days = int(period.split()[0])

    # Get data
    conversations = ConversationCRUD.get_recent_sentiment_data(user_id,
                                                               days=days)
    adherence = MedicationLogCRUD.get_medication_adherence(user_id, days=days)

    # Summary metrics
    st.subheader("📈 Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        if conversations:
            valid_sentiments = [
                c.sentiment_score for c in conversations
                if c.sentiment_score is not None
            ]

            if valid_sentiments:
                avg_mood = sum(valid_sentiments) / len(valid_sentiments)
                mood_emoji = get_sentiment_emoji(avg_mood)
                st.metric("Average Mood", f"{mood_emoji} {avg_mood:.2f}")
            else:
                st.metric("Average Mood", "No data")
        else:
            st.metric("Average Mood", "No data")

    with col2:
        st.metric("Medication Adherence",
                  f"{adherence.get('adherence_rate', 0):.1f}%")

    with col3:
        st.metric("Total Conversations", len(conversations))

    st.divider()

    # Charts
    if conversations:
        # Mood trend chart - convert to Central Time for proper date
        st.subheader("😊 Mood Trends")

        df_mood = pd.DataFrame([{
            "date": to_central(conv.timestamp).date(),
            "sentiment_score": conv.sentiment_score,
            "sentiment_label": conv.sentiment_label
        } for conv in conversations if conv.sentiment_score is not None])

        # Daily average mood
        daily_mood = df_mood.groupby(
            "date")["sentiment_score"].mean().reset_index()
        daily_mood["date"] = pd.to_datetime(daily_mood["date"])
        daily_mood["date_str"] = daily_mood["date"].dt.strftime('%b %d')

        # Create line chart with scatter to ensure points are visible
        fig_mood = px.line(daily_mood,
                           x="date",
                           y="sentiment_score",
                           title="Daily Average Mood",
                           range_y=[-1.1, 1.1],
                           markers=True)

        # Style the line - blue (#87CEEB) with prominent markers
        fig_mood.update_traces(line=dict(color='#87CEEB', width=3),
                               marker=dict(size=10,
                                           color='#87CEEB',
                                           line=dict(width=2, color='white')),
                               mode='lines+markers')

        fig_mood.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_mood.add_hline(y=0.3,
                           line_dash="dot",
                           line_color="green",
                           annotation_text="Good mood")
        fig_mood.add_hline(y=-0.3,
                           line_dash="dot",
                           line_color="red",
                           annotation_text="Concerning")

        fig_mood.update_layout(
            yaxis_title="Sentiment Score",
            xaxis_title="Date",
            showlegend=False,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=40, b=40, l=40, r=20),
            xaxis=dict(
                title_font=dict(color='black'),
                tickfont=dict(color='black')
            ),
            yaxis=dict(
                title_font=dict(color='black'),
                tickfont=dict(color='black')
            )
        )

        fig_mood.update_xaxes(
            showgrid=True, 
            gridcolor='lightgray',
            tickformat='%b %d',
            dtick='D1'
        )
        fig_mood.update_yaxes(showgrid=True, gridcolor='lightgray')

        st.plotly_chart(fig_mood, use_container_width=True)
    else:
        st.info(
            "No mood data available yet. Chat with Carely to track your mood over time!"
        )

    # Health recommendations
    st.subheader("💡 Health Recommendations")

    recommendations = []

    # --- Nurturing generic wellness guidance ---
    generic_nurturing_recs = [
        "💖 You're doing a wonderful job taking care of yourself. Even small healthy choices today really matter.",
        "🚶‍♀️ If it feels comfortable, try a short gentle walk or a few stretches. Moving a little can help your body feel lighter.",
        "💧 Remember to sip some water regularly today to stay refreshed and energized.",
        "🍲 A simple balanced meal with something you enjoy can make your body feel cared for.",
        "😴 A restful night's sleep is a gift to your mind and body — you deserve it.",
        "📞 A quick chat with someone you care about can brighten your whole day.",
        "🧩 Keep your brain active by doing something you enjoy like puzzles, reading, or knitting.",
        "🌞 A little sunlight or fresh air can help lift your spirits — even just by the window.",
        "🏡 Take a moment to make sure your walking areas are clear to help avoid a fall.",
        "💊 You're doing your best with your medications — keeping them in a labeled pillbox can help even more.",
        "💗 Don’t forget to be gentle with yourself today — you’re doing the best you can."
    ]

    # Analyze recent mood trends
    if conversations:
        recent_mood = [
            c.sentiment_score for c in conversations[-7:]
            if c.sentiment_score is not None
        ]
        if recent_mood:
            avg_recent_mood = sum(recent_mood) / len(recent_mood)
            if avg_recent_mood < -0.3:
                recommendations.append(
                    "🟡 You've had some tough moments lately. It might help to talk with someone who supports you — you're not alone. 💛"
                )
            elif avg_recent_mood > 0.3:
                recommendations.append(
                    "🟢 Your recent mood looks positive — keep up the lovely habits that are helping you feel good! 🌼"
                )

    # Medication adherence
    adherence_rate = adherence.get("adherence_rate", 100)
    if adherence_rate < 80:
        recommendations.append(
            "🔴 Medication has been a little hard to keep up with — maybe a few gentle reminders or an organized pillbox could help. 💊"
        )
    elif adherence_rate > 90:
        recommendations.append(
            "🟢 Wonderful medication routine ❤️ You're taking great care of yourself!"
        )

    # Engagement check
    if len(conversations) < 7 and days >= 7:
        recommendations.append(
            "🟡 Checking in with Carely a bit more often can help us support you better 💕"
        )

    # If nothing else applies — reassurance
    if not recommendations:
        recommendations.append(
            "🟢 Everything looks good right now — keep caring for yourself in these lovely ways! 🌷"
        )

    # Add 2 nurturing reminders to every set of recommendations
    import random
    extra_tips = random.sample(generic_nurturing_recs,
                               k=min(4, len(generic_nurturing_recs)))
    recommendations.extend(extra_tips)

    # Display
    for rec in recommendations:
        st.write(rec)

    # Soft senior-safety disclaimer
    st.caption(
        "ℹ️ These are gentle wellness tips — always follow your doctor's advice for medical needs."
    )


def show_alerts_and_reminders(user_id: int):
    """Show alerts and reminders interface"""
    user = UserCRUD.get_user(user_id)
    st.header(f"🚨 Alerts & Reminders - {user.name}")

    # Tabs for different types
    tab1, tab2, tab3 = st.tabs(
        ["🔔 Pending Reminders", "🚨 Active Alerts", "📋 Reminder History"])

    with tab1:
        st.subheader("Pending Reminders")

        reminders = ReminderCRUD.get_pending_reminders(user_id)

        if reminders:
            for reminder in reminders:
                with st.container():
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        # Color code by type
                        if reminder.reminder_type == "medication":
                            st.markdown(f"💊 **{reminder.title}**")
                        elif reminder.reminder_type == "checkin":
                            st.markdown(f"💬 **{reminder.title}**")
                        else:
                            st.markdown(f"📅 **{reminder.title}**")

                        st.write(reminder.message)
                        st.caption(
                            f"Scheduled: {format_time_central(reminder.scheduled_time, '%m/%d/%Y %I:%M %p')}"
                        )

                    with col2:
                        if st.button("✅ Complete",
                                     key=f"complete_{reminder.id}"):
                            ReminderCRUD.complete_reminder(reminder.id)
                            st.success("Reminder completed!")
                            st.rerun()

                    st.divider()
        else:
            st.info("No pending reminders")

    with tab2:
        st.subheader("Active Alerts")

        alerts = CaregiverAlertCRUD.get_unresolved_alerts(user_id)

        if alerts:
            for alert in alerts:
                with st.container():
                    # Color code by severity
                    if alert.severity == "high":
                        st.error(f"🔴 **{alert.title}**")
                    elif alert.severity == "medium":
                        st.warning(f"🟡 **{alert.title}**")
                    else:
                        st.info(f"🟢 **{alert.title}**")

                    st.write(alert.description)
                    st.caption(
                        f"Created: {format_time_central(alert.created_at, '%m/%d/%Y %I:%M %p')} | Type: {alert.alert_type}"
                    )

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("✅ Resolve", key=f"resolve_{alert.id}"):
                            CaregiverAlertCRUD.resolve_alert(alert.id)
                            st.success("Alert resolved!")
                            st.rerun()

                    st.divider()
        else:
            st.success("No active alerts - all good! ✨")

    with tab3:
        st.subheader("Reminder History")

        # This would show completed reminders and resolved alerts
        # For now, showing a simple message
        st.info("Reminder history feature coming soon!")

        # Could add filters for date range, type, etc.
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Filter by Type:",
                         ["All", "Medication", "Check-in", "Custom"])
        with col2:
            st.selectbox("Filter by Status:", ["All", "Completed", "Missed"])
        with col3:
            st.selectbox("Time Period:",
                         ["Last 7 days", "Last 30 days", "All time"])


def show_user_management():
    """Show user management interface"""
    st.header("👥 User Management")

    # Current users
    users = UserCRUD.get_all_users()

    if users:
        st.subheader("Current Users")

        for user in users:
            with st.expander(f"{user.name} (ID: {user.id})"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Name:** {user.name}")
                    st.write(f"**Email:** {user.email or 'Not provided'}")
                    st.write(f"**Phone:** {user.phone or 'Not provided'}")
                    st.write(
                        f"**Emergency Contact:** {user.emergency_contact or 'Not provided'}"
                    )

                with col2:
                    st.write(
                        f"**Created:** {format_time_central(user.created_at, '%m/%d/%Y')}"
                    )
                    if user.preferences:
                        try:
                            prefs = json.loads(user.preferences)
                            st.write("**Preferences:**")
                            for key, value in prefs.items():
                                st.write(f"- {key}: {value}")
                        except:
                            st.write("**Preferences:** Invalid format")

                    # Quick stats
                    conversations = ConversationCRUD.get_user_conversations(
                        user.id, limit=1)
                    medications = MedicationCRUD.get_user_medications(user.id)
                    st.write(f"**Medications:** {len(medications)}")
                    st.write(
                        f"**Last Chat:** {format_time_central(conversations[0].timestamp, '%m/%d/%Y') if conversations else 'Never'}"
                    )

    st.divider()

    # Add new user
    st.subheader("➕ Add New User")

    with st.form("add_user"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name*")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")

        with col2:
            emergency_contact = st.text_input("Emergency Contact")

            # Preferences
            st.write("**Preferences:**")
            pref_language = st.selectbox(
                "Preferred Language:",
                ["English", "Spanish", "French", "Other"])
            pref_time = st.selectbox(
                "Preferred Contact Time:",
                ["Morning", "Afternoon", "Evening", "Any"])
            pref_reminders = st.checkbox("Enable Reminders", value=True)

        if st.form_submit_button("Add User"):
            if name:
                try:
                    preferences = {
                        "language": pref_language,
                        "contact_time": pref_time,
                        "reminders_enabled": pref_reminders
                    }

                    new_user = UserCRUD.create_user(
                        name=name,
                        email=email or None,
                        phone=phone or None,
                        preferences=preferences,
                        emergency_contact=emergency_contact or None)

                    st.success(
                        f"Added user {name} successfully! (ID: {new_user.id})")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error adding user: {e}")
            else:
                st.error("Please enter a name")

    # User statistics
    if users:
        st.divider()
        st.subheader("📊 User Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Users", len(users))

        with col2:
            # Users with medications
            users_with_meds = 0
            for user in users:
                if MedicationCRUD.get_user_medications(user.id):
                    users_with_meds += 1
            st.metric("Users with Medications", users_with_meds)

        with col3:
            # Users with recent activity (last 7 days)
            active_users = 0
            for user in users:
                conversations = ConversationCRUD.get_user_conversations(
                    user.id, limit=1)
                if conversations and (now_central() -
                                      conversations[0].timestamp).days <= 7:
                    active_users += 1
            st.metric("Active Users (7d)", active_users)

        with col4:
            # Users with alerts
            users_with_alerts = 0
            for user in users:
                alerts = CaregiverAlertCRUD.get_unresolved_alerts(user.id)
                if alerts:
                    users_with_alerts += 1
            st.metric("Users with Alerts", users_with_alerts)
