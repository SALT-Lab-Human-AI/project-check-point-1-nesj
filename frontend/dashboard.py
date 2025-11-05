import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, time
import json
import os
import requests
import time as time_module
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
    """Apply elderly-friendly CSS styling with larger fonts and high contrast colors"""
    st.markdown("""
        <style>
        /* Import a clear, readable font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Force light theme */
        .stApp {
            background-color: #FFFFFF !important;
        }
        
        /* Global font settings - larger and clearer */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 18px !important;
            line-height: 1.6 !important;
            background-color: #FFFFFF !important;
        }
        
        /* Main content area - light background */
        .main {
            background-color: #FFFFFF !important;
            padding: 2rem;
        }
        
        .block-container {
            background-color: #FFFFFF !important;
            padding-top: 3rem;
        }
        
        /* Headings - larger and bolder */
        h1 {
            font-size: 2.8rem !important;
            font-weight: 700 !important;
            color: #FF8C69 !important;
            margin-bottom: 0.5rem !important;
            margin-top: 0 !important;
        }
        
        h2 {
            font-size: 2rem !important;
            font-weight: 600 !important;
            color: #2C3E50 !important;
            margin-top: 1.5rem !important;
        }
        
        h3 {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #5A6C7D !important;
            margin-top: 0.5rem !important;
        }
        
        /* Paragraphs and text */
        p, .stMarkdown {
            font-size: 1.1rem !important;
            color: #2C3E50 !important;
        }
        
        /* Sidebar styling - clean white */
        [data-testid="stSidebar"] {
            background-color: #F8F9FA !important;
            border-right: 3px solid #E8EAED;
            padding-top: 2rem;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #2C3E50 !important;
            font-size: 1.3rem !important;
        }
        
        /* Buttons - larger and more accessible */
        .stButton button {
            font-size: 1.2rem !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #FF8C69 0%, #FF6B47 100%) !important;
            color: white !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(255, 140, 105, 0.2);
            min-height: 70px !important;
            height: 70px !important;
            white-space: normal !important;
            line-height: 1.4 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #FF6B47 0%, #FF4D29 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(255, 140, 105, 0.3);
        }
        
        /* Primary buttons (send button) */
        .stButton button[kind="primary"],
        .stButton button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #FF8C69 0%, #FF6B47 100%) !important;
            color: white !important;
            min-height: 50px !important;
            height: 50px !important;
            font-size: 1.5rem !important;
            padding: 0 !important;
        }
        
        .stButton button[kind="primary"]:hover {
            background: linear-gradient(135deg, #FF6B47 0%, #FF4D29 100%) !important;
        }
        
        /* Text inputs - larger and clearer */
        .stTextInput input {
            font-size: 1.2rem !important;
            padding: 0.875rem 1rem !important;
            border-radius: 10px !important;
            border: 2px solid #E0E0E0 !important;
            background-color: #FFFFFF !important;
            color: #2C3E50 !important;
            caret-color: #FF8C69 !important;
            height: 50px !important;
            line-height: 1.5 !important;
        }
        
        .stTextInput input:focus {
            border-color: #FF8C69 !important;
            box-shadow: 0 0 0 3px rgba(255, 140, 105, 0.1) !important;
            caret-color: #FF8C69 !important;
        }
        
        /* Select boxes - larger */
        .stSelectbox select {
            font-size: 1.2rem !important;
            padding: 0.75rem !important;
            border-radius: 10px !important;
            background-color: #FFFFFF !important;
            color: #2C3E50 !important;
        }
        
        /* Radio buttons - larger and more spaced */
        .stRadio label {
            font-size: 1.2rem !important;
            padding: 0.75rem !important;
            margin-bottom: 0.5rem !important;
            color: #2C3E50 !important;
        }
        
        /* Chat messages - larger and clearer */
        .stChatMessage {
            font-size: 1.2rem !important;
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
            border-radius: 15px !important;
            background-color: #F8F9FA !important;
        }
        
        /* Mic button styling - match send button */
        button[kind="secondary"],
        .stButton button[kind="secondary"] {
            background: linear-gradient(135deg, #FF8C69 0%, #FF6B47 100%) !important;
            color: white !important;
            border: none !important;
            font-size: 1.5rem !important;
            min-height: 50px !important;
            height: 50px !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
            padding: 0 !important;
        }
        
        button[kind="secondary"]:hover,
        .stButton button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #FF6B47 0%, #FF4D29 100%) !important;
            transform: translateY(-2px);
        }
        

        
        /* Metrics - larger numbers */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #2C3E50 !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1.1rem !important;
            color: #5A6C7D !important;
        }
        
        /* Cards and containers */
        .element-container {
            margin-bottom: 1.5rem;
        }
        
        /* Dividers */
        hr {
            margin: 2rem 0 !important;
            border: none !important;
            border-top: 2px solid #E8EAED !important;
        }
        
        /* Success/Info/Warning boxes - high contrast */
        .stSuccess, .stInfo, .stWarning, .stError {
            font-size: 1.1rem !important;
            padding: 1rem 1.5rem !important;
            border-radius: 10px !important;
        }
        
        /* Remove dark theme artifacts */
        .stApp [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }
        
        /* High contrast color palette */
        .positive-sentiment {
            color: #27AE60 !important;
            font-weight: 600;
        }
        
        .negative-sentiment {
            color: #E74C3C !important;
            font-weight: 600;
        }
        
        .neutral-sentiment {
            color: #95A5A6 !important;
        }
        </style>
    """, unsafe_allow_html=True)


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
        # Add CSS to fix sidebar width and reduce spacing
        st.markdown("""
            <style>
            /* Fix sidebar width - disable resizing */
            [data-testid="stSidebar"] {
                width: 320px !important;
                min-width: 320px !important;
                max-width: 320px !important;
                overflow-y: hidden !important;
                padding-top: 0 !important;
            }
            
            [data-testid="stSidebar"] > div:first-child {
                width: 320px !important;
                min-width: 320px !important;
                max-width: 320px !important;
                overflow-y: hidden !important;
                padding-top: 0 !important;
            }
            
            /* Hide resize handle and sidebar header */
            [data-testid="stSidebar"] button[kind="header"] {
                display: none !important;
            }
            
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            
            /* Aggressive removal of all top spacing */
            section[data-testid="stSidebar"] {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            section[data-testid="stSidebar"] > div {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            section[data-testid="stSidebar"] > div > div:first-child {
                padding-top: 0 !important;
                margin-top: 0 !important;
                border-top: none !important;
            }
            
            [data-testid="stSidebar"] > div {
                padding-top: 0 !important;
                margin-top: 0 !important;
                border-top: none !important;
            }
            
            [data-testid="stSidebar"] .block-container {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            /* Remove spacing from first element container */
            [data-testid="stSidebar"] .element-container:first-child {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            /* Remove any borders at the top */
            [data-testid="stSidebar"]::before,
            [data-testid="stSidebar"] > div::before {
                display: none !important;
            }
            
            /* Center sidebar vertically with wrapper */
            section[data-testid="stSidebar"] {
                display: flex !important;
                align-items: center !important;
            }
            
            /* Add balanced padding to sidebar content - keep content together */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                padding-top: 1.5rem !important;
                padding-bottom: 1.5rem !important;
            }
            
            /* Reduce all sidebar spacing */
            [data-testid="stSidebar"] .element-container {
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
            }
            
            [data-testid="stSidebar"] .stSelectbox {
                margin-top: 0.2rem !important;
                margin-bottom: 0.2rem !important;
            }
            
            /* Vertically center selectbox content */
            [data-testid="stSidebar"] .stSelectbox > div > div {
                display: flex !important;
                align-items: center !important;
            }
            
            [data-testid="stSidebar"] .stSelectbox select {
                display: flex !important;
                align-items: center !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        logo_path = r"c:\Users\duvvu\Downloads\Logo.png"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, use_container_width=True)
            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-bottom: 0.1rem; margin-top: 0; font-size: 1.4rem; display: flex; align-items: center;'>👤 User</h3>", unsafe_allow_html=True)
        users = UserCRUD.get_all_users()

        if not users:
            st.error("No users found. Please add users first.")
            show_user_management()
            return

        user_options = {
            f"{user.name}": user.id
            for user in users
        }
        selected_user_key = st.selectbox("",
                                         list(user_options.keys()),
                                         label_visibility="collapsed")
        selected_user_id = user_options[selected_user_key]

        st.markdown("<div style='margin: 1.2rem 0;'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='margin-bottom: 0.2rem; margin-top: 0; font-size: 1.4rem; display: flex; align-items: center;'>📱 Navigation</h3>", unsafe_allow_html=True)
        
        # Add custom CSS for navigation tabs with boundaries
        st.markdown("""
            <style>
            /* Style radio buttons as tabs with uniform dimensions */
            div[role="radiogroup"] {
                gap: 0.4rem !important;
            }
            
            div[role="radiogroup"] label {
                border: 2px solid #E0E0E0 !important;
                border-radius: 10px !important;
                padding: 0.5rem 0.75rem !important;
                margin-bottom: 0.3rem !important;
                background: white !important;
                transition: all 0.3s ease !important;
                display: flex !important;
                align-items: center !important;
                width: 100% !important;
                min-height: 42px !important;
            }
            
            div[role="radiogroup"] label div {
                display: flex !important;
                align-items: center !important;
                gap: 0.5rem !important;
                line-height: 1 !important;
            }
            
            div[role="radiogroup"] label div p {
                margin: 0 !important;
                padding: 0 !important;
                line-height: 1.2 !important;
                display: inline-flex !important;
                align-items: center !important;
            }
            
            /* Align radio button circles with text */
            div[role="radiogroup"] label input[type="radio"] {
                margin-top: 0 !important;
                margin-bottom: 0 !important;
                margin-right: 0.5rem !important;
                align-self: center !important;
            }
            
            div[role="radiogroup"] label:hover {
                border-color: #FF8C69 !important;
                background: #FFF5F2 !important;
                transform: translateX(3px);
            }
            
            div[role="radiogroup"] label[data-checked="true"] {
                border-color: #FF8C69 !important;
                background: linear-gradient(135deg, #FFF5F2 0%, #FFE8E0 100%) !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 8px rgba(255, 140, 105, 0.2);
            }
            
            /* Remove extra spacing in radiogroup */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
                gap: 0 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        page = st.radio("",
                       [
                           "🏠 Overview", "💬 Chat with Carely", "💊 Medications",
                           "📊 Health Insights", "🚨 Alerts & Reminders"
                       ],
                       label_visibility="collapsed")

    # Main content based on selected page
    if page == "🏠 Overview":
        show_overview(selected_user_id)
    elif page == "💬 Chat with Carely":
        show_chat_interface(selected_user_id)
    elif page == "💊 Medications":
        show_medication_management(selected_user_id)
    elif page == "📊 Health Insights":
        show_health_insights(selected_user_id)
    elif page == "🚨 Alerts & Reminders":
        show_alerts_and_reminders(selected_user_id)


def get_upcoming_events_for_overview(user_id: int) -> List[Dict[str, Any]]:
    """
    Get the next 10 upcoming personal events from the database.
    Automatically refreshes based on current date/time.
    
    Returns:
        List of next 10 events sorted by datetime with formatted display strings
    """
    events = []
    
    # Get current time in Central Time
    current_time = now_central()
    
    # === PERSONAL EVENTS ===
    try:
        from app.database.models import PersonalEvent, get_session
        from sqlmodel import select
        
        with get_session() as session:
            # Query all future events for this user
            query = select(PersonalEvent).where(
                PersonalEvent.user_id == user_id,
                PersonalEvent.event_date.isnot(None)
            )
            personal_events = session.exec(query).all()
            
            for event in personal_events:
                # Convert to Central Time
                event_time = to_central(event.event_date)
                
                # Only include future events (from current time onwards)
                if event_time >= current_time:
                    # Determine if it's recurring
                    is_recurring = event.recurring if hasattr(event, 'recurring') else False
                    
                    # Map event type to emoji
                    emoji_map = {
                        'appointment': '📅',
                        'medication': '💊',
                        'birthday': '🎂',
                        'family_event': '👨‍👩‍👧‍👦',
                        'hobby': '🎨',
                        'achievement': '🏆',
                        'health': '🏥',
                        'social': '👥'
                    }
                    emoji = emoji_map.get(event.event_type, '📌')
                    
                    events.append({
                        'datetime': event_time,
                        'date_display': event_time.strftime('%A, %B %d'),
                        'time_display': event_time.strftime('%I:%M %p %Z'),
                        'emoji': emoji,
                        'title': event.title,
                        'description': event.description or '',
                        'type': event.event_type,
                        'is_recurring': is_recurring
                    })
    except Exception as e:
        # Silently fail if there's an error fetching personal events
        pass
    
    # Sort events by datetime and take only the next 10
    events.sort(key=lambda x: x['datetime'])
    
    return events[:10]  # Return only the next 10 upcoming events


def show_overview(user_id: int):
    """Show overview dashboard"""
    user = UserCRUD.get_user(user_id)
    if not user:
        st.error("User not found")
        return
    
    # Add CSS to remove top spacing on Overview page
    st.markdown("""
        <style>
        /* Force remove ALL top spacing from main content */
        .main .block-container,
        [data-testid="stAppViewContainer"] .main .block-container,
        section.main > div,
        .block-container {
            padding-top: 0rem !important;
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
        </style>
    """, unsafe_allow_html=True)

    # Get current time in Central Time for display
    current_time = now_central()
    current_day = current_time.strftime("%A")  # e.g., "Saturday"
    current_date = current_time.strftime("%B %d, %Y")  # e.g., "November 1, 2025"
    current_time_str = current_time.strftime("%I:%M %p %Z")  # e.g., "08:15 PM CST"
    
    # Page header without logo - very tight spacing with increased negative margin
    st.markdown(f"""
        <div style='padding: 0; margin: -5rem 0 0 0; margin-bottom: 0;'>
            <h1 style='margin: 0; padding: 0; color: #FF8C69; font-size: 2rem;'>Carely: Your AI Companion</h1>
            <p style='margin: 0.2rem 0 0 0; font-size: 1.1rem; color: #5A6C7D; font-style: italic;'>Your caring companion, always here for you</p>
            <p style='margin: 0.3rem 0 0 0; font-size: 0.95rem; color: #95A5A6;'>📅 {current_day}, {current_date} • 🕐 {current_time_str}</p>
            <h2 style='margin: 0.5rem 0 0.2rem 0; color: #333; font-size: 1.5rem;'>👋 Hello, {user.name}!</h2>
            <p style='margin: 0; font-size: 1rem; color: #666; font-weight: 500;'>Here's your summary for today</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)

    # Today's summary cards with better styling
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white;'>
                <h3 style='color: white; margin: 0;'>👤 Profile</h3>
                <h2 style='color: white; margin-top: 0.5rem;'>{}</h2>
            </div>
        """.format(user.name), unsafe_allow_html=True)

    with col2:
        # Medication adherence today
        adherence = MedicationLogCRUD.get_medication_adherence(user_id, days=1)
        adherence_rate = adherence.get("adherence_rate", 0)
        color = "#27AE60" if adherence_rate >= 80 else "#E67E22" if adherence_rate >= 50 else "#E74C3C"
        st.markdown("""
            <div style='background: {}; padding: 1.5rem; border-radius: 15px; color: white;'>
                <h3 style='color: white; margin: 0;'>💊 Medications</h3>
                <h2 style='color: white; margin-top: 0.5rem;'>{}%</h2>
                <p style='color: white; margin: 0; opacity: 0.9;'>{}/{} doses taken</p>
            </div>
        """.format(color, int(adherence_rate), adherence.get('taken', 0), adherence.get('total', 0)), unsafe_allow_html=True)

    with col3:
        # Recent mood
        conversations = ConversationCRUD.get_recent_sentiment_data(user_id, days=1)
        if conversations:
            avg_mood = sum(c.sentiment_score
                           for c in conversations if c.sentiment_score) / len(
                               [c for c in conversations if c.sentiment_score])
            mood_emoji = get_sentiment_emoji(avg_mood)
            mood_color = "#27AE60" if avg_mood > 0.3 else "#E67E22" if avg_mood > -0.3 else "#E74C3C"
            st.markdown("""
                <div style='background: {}; padding: 1.5rem; border-radius: 15px; color: white;'>
                    <h3 style='color: white; margin: 0;'>😊 Mood</h3>
                    <h2 style='color: white; margin-top: 0.5rem;'>{} {:.2f}</h2>
                </div>
            """.format(mood_color, mood_emoji, avg_mood), unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background: #95A5A6; padding: 1.5rem; border-radius: 15px; color: white;'>
                    <h3 style='color: white; margin: 0;'>😊 Mood</h3>
                    <h2 style='color: white; margin-top: 0.5rem;'>No data</h2>
                </div>
            """, unsafe_allow_html=True)

    with col4:
        # Unresolved alerts
        alerts = CaregiverAlertCRUD.get_unresolved_alerts(user_id)
        alert_count = len(alerts)
        st.metric("🚨 Active Alerts", alert_count)

    # Upcoming Important Events Panel - minimal top spacing
    st.markdown("<div style='margin: 0.8rem 0 0.3rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin: 0; color: #333;'>🎯 Next 10 Upcoming Events</h3>", unsafe_allow_html=True)
    st.markdown("<div style='margin: 0.3rem 0;'></div>", unsafe_allow_html=True)
    
    # Get upcoming events using helper function
    upcoming_events = get_upcoming_events_for_overview(user_id)
    
    if upcoming_events:
        for event in upcoming_events:
            with st.container():
                col_time, col_info = st.columns([1, 3])
                
                with col_time:
                    st.write(f"**{event['time_display']}**")
                    st.caption(event['date_display'])
                
                with col_info:
                    # Display title with emoji
                    st.write(f"{event['emoji']} **{event['title']}**")
                    
                    # Show description if available (truncate if too long)
                    if event.get("description"):
                        desc = event["description"]
                        if len(desc) > 80:
                            desc = desc[:77] + "..."
                        st.write(f"_{desc}_")
                    
                    # Show recurring badge
                    if event.get("is_recurring"):
                        st.caption("� Recurring")
                
                st.divider()
    else:
        st.info("📭 No upcoming events scheduled.")

    # Recent Conversations - Full Width - minimal spacing
    st.markdown("<div style='margin: 0.8rem 0 0.3rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin: 0; color: #333;'>💬 Recent Conversations</h3>", unsafe_allow_html=True)
    st.markdown("<div style='margin: 0.3rem 0;'></div>", unsafe_allow_html=True)

    recent_conversations = ConversationCRUD.get_user_conversations(user_id, limit=10)

    if recent_conversations:
        # Create a more spacious layout with cards
        for conv in recent_conversations:
            with st.container():
                # Show sentiment with color
                sentiment_color = get_sentiment_color(conv.sentiment_score or 0)
                sentiment_emoji = get_sentiment_emoji(conv.sentiment_score or 0)

                # Always convert to Central Time for display (handles naive UTC timestamps from DB)
                display_time = to_central(conv.timestamp)
                
                # Create a nice card layout
                st.markdown(f"""
                    <div style='background-color: #F8F9FA; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #FF8C69;'>
                        <p style='color: #5A6C7D; font-size: 0.9rem; margin: 0;'>
                            <strong>{display_time.strftime('%I:%M %p')}</strong> {sentiment_emoji}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**You:** {conv.message}")
                with col2:
                    st.markdown(f"**Carely:** {conv.response}")
                
                st.divider()
    else:
        st.info("No recent conversations. Start chatting with Carely to see your conversation history here!")


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
    import time as time_module
    
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
        "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸"],
        "fruits": ["🍎", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍑", "🍒", "🍍", "🥝", "🥭", "🍐", "🥥"],
        "flowers": ["🌸", "🌺", "🌻", "🌷", "🌹", "🥀", "🌼", "🏵️", "💐", "🌲", "🌳", "🌴", "🌱", "🍀"]
    }
    
    # Determine grid size based on level
    level_config = {
        1: {"pairs": 2, "grid": (2, 2)},   # 4 cards
        2: {"pairs": 4, "grid": (2, 4)},   # 8 cards
        3: {"pairs": 6, "grid": (3, 4)},   # 12 cards
        4: {"pairs": 8, "grid": (4, 4)}    # 16 cards
    }
    
    current_config = level_config.get(st.session_state.game_level, level_config[1])
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
    if not st.session_state.game_deck or len(st.session_state.game_deck) != pairs_needed * 2:
        st.session_state.game_deck = initialize_deck()
        st.session_state.revealed_cards = []
        st.session_state.matched_cards = set()
        st.session_state.moves_count = 0
        st.session_state.game_start_time = time_module.time()
        st.session_state.check_mismatch = False
    
    # Calculate elapsed time
    elapsed_time = 0
    if st.session_state.game_start_time:
        elapsed_time = int(time_module.time() - st.session_state.game_start_time)
    
    # HUD - Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Level", st.session_state.game_level)
    with col2:
        st.metric("✨ Pairs Found", f"{len(st.session_state.matched_cards)}/{pairs_needed}")
    with col3:
        st.metric("🔄 Moves", st.session_state.moves_count)
    with col4:
        st.metric("⏱️ Time", f"{elapsed_time}s")
    
    st.markdown("---")
    
    # Check if game is won
    if len(st.session_state.matched_cards) == pairs_needed:
        st.success(f"🎉 Congratulations! You completed Level {st.session_state.game_level}!")
        st.balloons()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.game_level < 4:
                if st.button("➡️ Next Level", key="next_level", use_container_width=True):
                    st.session_state.game_level += 1
                    st.session_state.game_deck = []
                    st.rerun()
            else:
                st.info("🏆 You've completed all levels!")
        
        with col2:
            if st.button("🔄 Restart Level", key="restart_same", use_container_width=True):
                st.session_state.game_deck = []
                st.rerun()
        
        with col3:
            if st.button("🏠 Back to Chat", key="back_to_chat_win", use_container_width=True):
                st.session_state.show_memory_game = False
                st.rerun()
        return
    
    # Game controls
    st.markdown("### 🎴 Game Board")
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        if st.button("🔄 Restart Level", key="restart_game", use_container_width=True):
            st.session_state.game_deck = []
            st.rerun()
    
    with col2:
        theme_options = list(themes.keys())
        selected_theme = st.selectbox(
            "Theme", 
            theme_options, 
            index=theme_options.index(st.session_state.game_theme),
            key="theme_select"
        )
        if selected_theme != st.session_state.game_theme:
            st.session_state.game_theme = selected_theme
            st.session_state.game_deck = []
            st.rerun()
    
    with col3:
        if st.button("🏠 Back to Chat", key="back_to_chat", use_container_width=True):
            st.session_state.show_memory_game = False
            st.rerun()
    
    st.markdown("---")
    
    # Handle mismatch delay (flip back after showing)
    if st.session_state.check_mismatch and len(st.session_state.revealed_cards) == 2:
        idx1, idx2 = st.session_state.revealed_cards
        if st.session_state.game_deck[idx1] != st.session_state.game_deck[idx2]:
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
                    """, unsafe_allow_html=True)
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
                    """, unsafe_allow_html=True)
                else:
                    # Facedown card - clickable
                    if st.button("❓", key=f"card_{card_idx}", use_container_width=True):
                        # Can only reveal if less than 2 cards are shown
                        if len(st.session_state.revealed_cards) < 2:
                            st.session_state.revealed_cards.append(card_idx)
                            
                            # Check if two cards are revealed
                            if len(st.session_state.revealed_cards) == 2:
                                st.session_state.moves_count += 1
                                idx1, idx2 = st.session_state.revealed_cards
                                
                                # Check if they match
                                if st.session_state.game_deck[idx1] == st.session_state.game_deck[idx2]:
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
    st.header(f"💬 Chat with Carely - {user.name}")

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
            time_since_last = (now_central() - last_conv_time).total_seconds() / 3600  # hours
            if time_since_last > 4:  # More than 4 hours since last conversation
                should_greet = True
        
        if should_greet and not st.session_state.proactive_greeting_sent:
            try:
                proactive_message = st.session_state.companion_agent.generate_proactive_greeting(user_id)
                if proactive_message:
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": proactive_message,
                        "timestamp": now_central(),
                        "is_proactive": True
                    })
                    
                    # Save to database
                    ConversationCRUD.save_conversation(
                        user_id=user_id,
                        message="[Proactive Greeting]",
                        response=proactive_message,
                        conversation_type="proactive_greeting"
                    )
                    
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

    # Chat container
    chat_container = st.container()

    # Initialize TTS state
    if 'playing_audio' not in st.session_state:
        st.session_state.playing_audio = None

    with chat_container:
        # Display chat history
        for idx, message in enumerate(
                st.session_state.chat_history[-10:]):  # Show last 10 messages
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar="🏥"):
                    msg_col1, msg_col2 = st.columns([9, 1])

                    with msg_col1:
                        content = message["content"]

                        # Check if message contains YouTube URL and embed it
                        if "youtube.com/watch?v=" in content or "youtu.be/" in content:
                            lines = content.split("\n")
                            text_lines = []
                            video_url = None

                            for line in lines:
                                if "youtube.com/watch?v=" in line or "youtu.be/" in line:
                                    video_url = line.strip()
                                else:
                                    text_lines.append(line)

                            # Display text first
                            st.write("\n".join(text_lines))

                            # Embed YouTube video
                            if video_url:
                                st.video(video_url)
                        else:
                            st.write(content)

                    with msg_col2:
                        if st.button("🔊",
                                     key=f"listen_{idx}",
                                     help="Listen to this message"):
                            st.session_state.playing_audio = idx
                            st.rerun()

                    if st.session_state.playing_audio == idx:
                        audio_bytes = generate_speech_audio(message["content"],
                                                            slow=True)
                        if audio_bytes:
                            st.audio(audio_bytes,
                                     format='audio/mp3',
                                     autoplay=True)
                            st.session_state.playing_audio = None

                    # Quick Actions are now shown persistently above input - removed from chat history

    # Handle quick action button clicks
    if st.session_state.get("pending_action"):
        action = st.session_state.pending_action
        st.session_state.pending_action = None

        if action == "log_medication":
            # Find the most recent reminder with medication_id
            medication_id = None
            for msg in reversed(st.session_state.chat_history):
                if msg.get("reminder_id") and msg.get("medication_id"):
                    medication_id = msg.get("medication_id")
                    break

            # Log medication with duplicate detection
            response_text = st.session_state.companion_agent.log_medication_tool(
                user_id=user_id, medication_id=medication_id)
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

    # Integrated input bar with voice and text
    st.markdown("---")
    st.markdown("##### Type or speak your message:")

    # Add CSS to align all input elements properly
    st.markdown("""
        <style>
        /* Align all input row elements */
        div[data-testid="column"] {
            display: flex !important;
            align-items: flex-end !important;
        }
        
        /* Ensure text input aligns with buttons */
        div[data-testid="stTextInput"] {
            margin-bottom: 0 !important;
        }
        
        /* Match mic button iframe height to other buttons */
        iframe[title="streamlit_mic_recorder.speech_to_text"] {
            height: 50px !important;
            margin-bottom: 0 !important;
        }
        
        /* Ensure send button aligns */
        div[data-testid="column"] > div > div > button {
            margin-bottom: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create columns for text input, send button, and mic button side by side
    text_col, send_col, mic_col = st.columns([8, 1, 1], gap="small")
    
    prompt = None
    is_voice = False
    
    with text_col:
        # Initialize or get the current input value
        if f'clear_input_{user_id}' in st.session_state and st.session_state[f'clear_input_{user_id}']:
            st.session_state[f'chat_text_{user_id}'] = ""
            st.session_state[f'clear_input_{user_id}'] = False
        
        # Text input
        text_input = st.text_input(
            "Message",
            placeholder=f"Type your message here, {user.name}...",
            key=f"chat_text_{user_id}",
            label_visibility="collapsed"
        )
    
    with send_col:
        # Send button
        send_clicked = st.button("➤", key=f"send_btn_{user_id}", use_container_width=True, type="primary")
    
    with mic_col:
        # Compact mic button beside the chat input  
        voice_text = speech_to_text(language='en',
                                    start_prompt="🎤",
                                    stop_prompt="⏹️",
                                    just_once=True,
                                    use_container_width=True,
                                    key=f'voice_input_{user_id}')
    
    # Persistent Quick Actions - Below chat input for easy access
    st.markdown("")  # Add small spacing
    st.markdown("**Quick Actions:**")
    
    # Use equal columns with spacing
    action_col1, action_col2, action_col3, action_col4, action_col5 = st.columns(5, gap="medium")
    
    with action_col1:
        if st.button("🕐 Log Medication", key="persistent_log_med", use_container_width=True):
            st.session_state.pending_action = "log_medication"
            st.rerun()
    
    with action_col2:
        if st.button("🎵 Play Music", key="persistent_play_music", use_container_width=True):
            st.session_state.pending_action = "play_music"
            st.rerun()
    
    with action_col3:
        if st.button("🧩 Fun Corner", key="persistent_fun_corner", use_container_width=True):
            st.session_state.pending_action = "fun_corner"
            st.rerun()
    
    with action_col4:
        if st.button("🧠 Memory Cue", key="persistent_memory_cue", use_container_width=True):
            st.session_state.pending_action = "memory_cue"
            st.rerun()
    
    with action_col5:
        if st.button("🎮 Memory Game", key="persistent_memory_game", use_container_width=True):
            st.session_state.show_memory_game = True
            st.rerun()

    # Handle Enter key press using session state
    if text_input and text_input != st.session_state.get(f'last_input_{user_id}', ''):
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
        display_message = f"🎤 {prompt}" if is_voice else prompt

        with st.chat_message("user"):
            st.write(display_message)

        # Generate AI response
        with st.chat_message("assistant", avatar="🏥"):
            with st.spinner("Carely is thinking..."):
                response_data = st.session_state.companion_agent.generate_response(
                    user_id=user_id, user_message=prompt)

            st.write(response_data["response"])

            # Show sentiment if available
            if response_data.get("sentiment_score") is not None:
                sentiment_emoji = get_sentiment_emoji(
                    response_data["sentiment_score"])
                st.caption(
                    f"Detected mood: {sentiment_emoji} {response_data['sentiment_label']}"
                )

        # Update session state
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
                "severity": response_data.get("emergency_severity", "medium"),
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
    st.header(f"💊 Medication Management - {user.name}")

    # Medication overview
    medications = MedicationCRUD.get_user_medications(user_id)

    if medications:
        st.subheader("Current Medications")

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

    st.divider()

    # Medication adherence chart
    st.subheader("📊 Adherence Overview")

    # Time period selector
    period = st.selectbox("Select period:", ["Last 7 days", "Last 30 days"],
                          key="adherence_period")
    days = 7 if period == "Last 7 days" else 30

    adherence = MedicationLogCRUD.get_medication_adherence(user_id, days=days)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Doses", adherence.get("total", 0))
    with col2:
        st.metric("Doses Taken", adherence.get("taken", 0))
    with col3:
        st.metric("Adherence Rate",
                  f"{adherence.get('adherence_rate', 0):.1f}%")

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
        daily_adherence = df.groupby("date").apply(lambda x: (x[
            "status"] == "taken").sum() / len(x) * 100).reset_index(
                name="adherence_rate")
        daily_adherence["date"] = pd.to_datetime(daily_adherence["date"])

        fig = px.line(daily_adherence,
                      x="date",
                      y="adherence_rate",
                      title=f"Daily Adherence Rate ({period})",
                      range_y=[0, 100])
        fig.add_hline(y=80,
                      line_dash="dash",
                      line_color="orange",
                      annotation_text="Target: 80%")
        fig.update_layout(yaxis_title="Adherence Rate (%)", xaxis_title="Date")

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Add new medication
    st.subheader("➕ Add New Medication")

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if conversations:
            avg_mood = sum(c.sentiment_score
                           for c in conversations if c.sentiment_score) / len(
                               [c for c in conversations if c.sentiment_score])
            mood_emoji = get_sentiment_emoji(avg_mood)
            st.metric("Average Mood", f"{mood_emoji} {avg_mood:.2f}")
        else:
            st.metric("Average Mood", "No data")

    with col2:
        st.metric("Medication Adherence",
                  f"{adherence.get('adherence_rate', 0):.1f}%")

    with col3:
        st.metric("Total Conversations", len(conversations))

    with col4:
        alerts = CaregiverAlertCRUD.get_unresolved_alerts(user_id)
        st.metric("Active Concerns", len(alerts))

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

        fig_mood = px.line(daily_mood,
                           x="date",
                           y="sentiment_score",
                           title="Daily Average Mood",
                           range_y=[-1, 1])
        fig_mood.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_mood.add_hline(y=0.3,
                           line_dash="dot",
                           line_color="green",
                           annotation_text="Good mood")
        fig_mood.add_hline(y=-0.3,
                           line_dash="dot",
                           line_color="red",
                           annotation_text="Concerning")

        st.plotly_chart(fig_mood, use_container_width=True)

    # Health recommendations
    st.subheader("💡 Health Recommendations")

    recommendations = []

    if conversations:
        recent_mood = [
            c.sentiment_score for c in conversations[-7:]
            if c.sentiment_score is not None
        ]
        if recent_mood:
            avg_recent_mood = sum(recent_mood) / len(recent_mood)
            if avg_recent_mood < -0.3:
                recommendations.append(
                    "🟡 Recent mood trends show concern. Consider scheduling a check-in with healthcare provider."
                )
            elif avg_recent_mood > 0.3:
                recommendations.append(
                    "🟢 Mood trends are positive! Keep up the good routine.")

    if adherence.get("adherence_rate", 100) < 80:
        recommendations.append(
            "🔴 Medication adherence is below 80%. Consider setting more reminders or reviewing medication schedule."
        )
    elif adherence.get("adherence_rate", 100) > 90:
        recommendations.append(
            "🟢 Excellent medication adherence! Keep up the great work.")

    if len(conversations) < 7 and days >= 7:
        recommendations.append(
            "🟡 Consider chatting with Carely more regularly for better mood tracking."
        )

    if not recommendations:
        recommendations.append(
            "🟢 All health metrics look good! Continue current routine.")

    for rec in recommendations:
        st.write(rec)


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
