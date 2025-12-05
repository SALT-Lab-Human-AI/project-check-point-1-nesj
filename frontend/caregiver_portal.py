import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from typing import List

from app.database.crud import (
    UserCRUD, CaregiverPatientCRUD, CaregiverAlertCRUD,
    MedicationLogCRUD, ConversationCRUD
)
from app.auth.auth_utils import authenticate_user
from utils.sentiment_analysis import get_sentiment_emoji, get_sentiment_color

def show_caregiver_login():
    """Show caregiver login page"""
    st.title("🏥 Caregiver Portal - Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = authenticate_user(email, password)
            if user and user.user_type in ["caregiver", "admin"]:
                st.session_state.caregiver_id = user.id
                st.session_state.caregiver_name = user.name
                st.session_state.caregiver_type = user.user_type
                st.success(f"Welcome back, {user.name}!")
                st.rerun()
            else:
                st.error("Invalid credentials or insufficient permissions")

def show_caregiver_dashboard():
    """Show caregiver dashboard"""
    caregiver_id = st.session_state.get("caregiver_id")
    
    if not caregiver_id:
        show_caregiver_login()
        return
    
    st.title(f"👨‍⚕️ Caregiver Portal - {st.session_state.get('caregiver_name')}")
    
    # Logout button
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("Logout"):
            del st.session_state.caregiver_id
            del st.session_state.caregiver_name
            del st.session_state.caregiver_type
            st.rerun()
    
    # Get assigned patients
    patients = CaregiverPatientCRUD.get_caregiver_patients(caregiver_id)
    
    if not patients:
        st.info("No patients assigned yet. Contact your administrator to assign patients.")
        return
    
    # Patient selector
    patient_options = {f"{p.name} (ID: {p.id})": p.id for p in patients}
    selected_patient_key = st.selectbox("Select Patient:", list(patient_options.keys()))
    selected_patient_id = patient_options[selected_patient_key]
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🚨 Alerts", 
        "💊 Medications",
        "💬 Conversations"
    ])
    
    with tab1:
        show_patient_overview(selected_patient_id)
    
    with tab2:
        show_patient_alerts(selected_patient_id)
    
    with tab3:
        show_patient_medications(selected_patient_id)
    
    with tab4:
        show_patient_conversations(selected_patient_id)

def show_patient_overview(patient_id: int):
    """Show patient overview for caregiver"""
    patient = UserCRUD.get_user(patient_id)
    
    st.subheader(f"Overview for {patient.name}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        adherence = MedicationLogCRUD.get_medication_adherence(patient_id, days=7)
        st.metric("7-Day Adherence", f"{adherence.get('adherence_rate', 0):.0f}%")
    
    with col2:
        conversations = ConversationCRUD.get_recent_sentiment_data(patient_id, days=7)
        if conversations:
            avg_mood = sum(c.sentiment_score for c in conversations if c.sentiment_score) / len([c for c in conversations if c.sentiment_score])
            mood_emoji = get_sentiment_emoji(avg_mood)
            st.metric("Avg Mood (7d)", f"{mood_emoji} {avg_mood:.2f}")
        else:
            st.metric("Avg Mood (7d)", "No data")
    
    with col3:
        alerts = CaregiverAlertCRUD.get_unresolved_alerts(patient_id)
        high_priority = len([a for a in alerts if a.severity == "high"])
        st.metric("Active Alerts", len(alerts), delta=f"{high_priority} high priority" if high_priority > 0 else None)
    
    with col4:
        missed_meds = adherence.get("missed", 0)
        st.metric("Missed Doses (7d)", missed_meds, delta=f"-{missed_meds}" if missed_meds > 0 else None)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Medication Adherence Trend")
        if adherence.get("logs"):
            df = pd.DataFrame([
                {
                    "date": log.scheduled_time.date(),
                    "status": "Taken" if log.status == "taken" else "Missed"
                }
                for log in adherence["logs"]
            ])
            
            daily_adherence = df.groupby("date").apply(
                lambda x: (x["status"] == "Taken").sum() / len(x) * 100
            ).reset_index(name="adherence_rate")
            daily_adherence["date"] = pd.to_datetime(daily_adherence["date"])
            
            fig = px.line(
                daily_adherence, 
                x="date", 
                y="adherence_rate",
                range_y=[0, 100]
            )
            fig.add_hline(y=80, line_dash="dash", line_color="orange")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No medication data available")
    
    with col2:
        st.subheader("Mood Trend")
        if conversations:
            df_mood = pd.DataFrame([
                {
                    "date": conv.timestamp.date(),
                    "sentiment_score": conv.sentiment_score
                }
                for conv in conversations
                if conv.sentiment_score is not None
            ])
            
            daily_mood = df_mood.groupby("date")["sentiment_score"].mean().reset_index()
            daily_mood["date"] = pd.to_datetime(daily_mood["date"])
            
            fig = px.line(
                daily_mood, 
                x="date", 
                y="sentiment_score",
                range_y=[-1, 1]
            )
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No mood data available")

def show_patient_alerts(patient_id: int):
    """Show patient alerts for caregiver"""
    st.subheader("Patient Alerts")
    
    alerts = CaregiverAlertCRUD.get_unresolved_alerts(patient_id)
    
    if not alerts:
        st.success("No active alerts!")
        return
    
    # Filter options
    severity_filter = st.multiselect(
        "Filter by severity:",
        ["low", "medium", "high"],
        default=["medium", "high"]
    )
    
    filtered_alerts = [a for a in alerts if a.severity in severity_filter]
    
    for alert in filtered_alerts:
        severity_color = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }.get(alert.severity, "⚪")
        
        with st.expander(f"{severity_color} {alert.title} - {alert.created_at.strftime('%m/%d %I:%M %p')}"):
            st.write(f"**Type:** {alert.alert_type}")
            st.write(f"**Severity:** {alert.severity}")
            st.write(f"**Description:**")
            st.write(alert.description)
            
            if st.button("Mark as Resolved", key=f"resolve_{alert.id}"):
                CaregiverAlertCRUD.resolve_alert(alert.id)
                st.success("Alert resolved!")
                st.rerun()

def show_patient_medications(patient_id: int):
    """Show patient medications for caregiver"""
    st.subheader("Medication Schedule & History")
    
    from app.database.crud import MedicationCRUD
    import json
    
    medications = MedicationCRUD.get_user_medications(patient_id)
    
    if not medications:
        st.info("No medications on file")
        return
    
    for med in medications:
        with st.expander(f"{med.name} - {med.dosage}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Frequency:** {med.frequency}")
                if med.schedule_times:
                    times = json.loads(med.schedule_times)
                    st.write(f"**Schedule:** {', '.join(times)}")
                if med.instructions:
                    st.write(f"**Instructions:** {med.instructions}")
            
            with col2:
                adherence = MedicationLogCRUD.get_medication_adherence(patient_id, days=7)
                med_logs = [log for log in adherence.get("logs", []) if log.medication_id == med.id]
                
                if med_logs:
                    st.write("**Recent Activity (Last 7 days):**")
                    for log in med_logs[-5:]:
                        status_emoji = "✅" if log.status == "taken" else "❌"
                        st.write(f"{status_emoji} {log.scheduled_time.strftime('%m/%d %I:%M %p')}")

def show_patient_conversations(patient_id: int):
    """Show patient conversations for caregiver"""
    st.subheader("Recent Conversations")
    
    conversations = ConversationCRUD.get_user_conversations(patient_id, limit=20)
    
    if not conversations:
        st.info("No conversations yet")
        return
    
    for conv in conversations:
        sentiment_emoji = get_sentiment_emoji(conv.sentiment_score or 0)
        sentiment_color = get_sentiment_color(conv.sentiment_score or 0)
        
        with st.expander(f"{sentiment_emoji} {conv.timestamp.strftime('%m/%d %I:%M %p')} - {conv.conversation_type}"):
            st.write(f"**Patient:** {conv.message}")
            st.write(f"**Carely:** {conv.response}")
            
            if conv.sentiment_score is not None:
                st.caption(f"Mood: {conv.sentiment_label} (score: {conv.sentiment_score:.2f})")
