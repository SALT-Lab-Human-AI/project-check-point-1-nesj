"""
Multi-step onboarding wizard for new users
"""
import streamlit as st
from datetime import datetime, date, time
import json
import os

from app.database.crud import UserCRUD, MedicationCRUD, PersonalEventCRUD, CaregiverPatientCRUD
from app.auth.auth_repository import AuthRepository, create_or_update_profile
from utils.timezone_utils import now_central, to_central


def show_onboarding_wizard():
    """Display multi-step onboarding wizard"""
    st.markdown("""
        <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
        
        /* Light gradient background matching Overview page */
        .stApp {
            background: linear-gradient(135deg, 
                #FFF5F7 0%,
                #FFF9F5 25%,
                #FFFEF5 50%,
                #F5FFFA 75%,
                #F8F5FF 100%
            ) !important;
            background-attachment: fixed !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Global font settings - dark text for light background */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: #4A5568 !important;
        }
        
        /* Remove ALL top spacing */
        body, html {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        .main .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
            background: transparent !important;
        }
        
        .main {
            background: transparent !important;
        }
        
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] .main,
        [data-testid="stAppViewContainer"] .main .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
            background: transparent !important;
        }
        
        /* Remove spacing from vertical blocks */
        [data-testid="stVerticalBlock"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
            gap: 0.3rem !important;
        }
        
        [data-testid="stVerticalBlock"]:first-child,
        [data-testid="stVerticalBlock"] > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Remove spacing from element containers */
        [data-testid="element-container"],
        [data-testid="element-container"]:first-child,
        [data-testid="element-container"] > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Remove spacing from markdown containers */
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"]:first-child,
        [data-testid="stMarkdownContainer"] > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        .onboarding-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 0.5rem 2rem 2rem 2rem !important;
            margin-top: 0 !important;
        }
        
        /* Headings with dark text for light background */
        h1, h2, h3, h4 {
            color: #2D3436 !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
        }
        
        h3 {
            font-size: 1.4rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Paragraphs with readable dark text */
        p {
            color: #4A5568 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .onboarding-container h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        .onboarding-container p {
            margin-top: 0.3rem !important;
        }
        
        /* Step indicator styling - updated for light theme */
        .step-indicator {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            margin-top: 0.5rem !important;
        }
        
        .step {
            flex: 1;
            text-align: center;
            padding: 1rem;
            border-radius: 12px;
            background: #FFFFFF;
            margin: 0 0.5rem;
            color: #4A5568;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 2px solid rgba(102, 126, 234, 0.1);
        }
        
        .step.active {
            background: linear-gradient(135deg, #FF6B6B 0%, #E76F51 100%);
            color: white;
            font-weight: bold;
            border: none;
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
        }
        
        .step.completed {
            background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
            color: white;
            border: none;
            box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
        }
        
        /* Labels with dark text */
        label, .stTextInput label, [data-testid="stTextInput"] label,
        [data-testid="stDateInput"] label, [data-testid="stTimeInput"] label,
        [data-testid="stSelectbox"] label {
            color: #2D3436 !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Input fields with light background */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stDateInput"] input,
        [data-testid="stTimeInput"] input {
            background-color: #FFFFFF !important;
            border: 1.5px solid rgba(102, 126, 234, 0.3) !important;
            border-radius: 8px !important;
            color: #2D3436 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: #667EEA !important;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.15) !important;
        }
        
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: #A0AEC0 !important;
        }
        
        /* Select box styling */
        [data-testid="stSelectbox"] > div > div {
            background-color: #FFFFFF !important;
            border: 1.5px solid rgba(102, 126, 234, 0.3) !important;
            color: #2D3436 !important;
        }
        
        /* Checkbox styling */
        [data-testid="stCheckbox"] label {
            color: #4A5568 !important;
        }
        
        [data-testid="stCheckbox"] label span {
            color: #4A5568 !important;
        }
        
        /* Tab styling */
        [data-testid="stTabs"] button {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            color: #4A5568 !important;
            background: transparent !important;
        }
        
        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #FF6B6B !important;
            border-bottom-color: #FF6B6B !important;
        }
        
        /* Expander styling */
        [data-testid="stExpander"] {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(102, 126, 234, 0.2) !important;
            border-radius: 8px !important;
        }
        
        [data-testid="stExpander"] summary {
            color: #2D3436 !important;
        }
        
        /* Alert styling */
        .stAlert {
            border-radius: 8px !important;
        }
        
        .stAlert[data-baseweb*="info"] {
            background-color: rgba(102, 126, 234, 0.1) !important;
            border-left: 4px solid #667EEA !important;
        }
        
        .stAlert[data-baseweb*="info"] p {
            color: #2D3436 !important;
        }
        
        .stAlert[data-baseweb*="negative"] {
            background-color: rgba(231, 76, 60, 0.1) !important;
            border-left: 4px solid #E74C3C !important;
        }
        
        .stAlert[data-baseweb*="negative"] p {
            color: #C0392B !important;
        }
        
        .stAlert[data-baseweb*="positive"] {
            background-color: rgba(39, 174, 96, 0.1) !important;
            border-left: 4px solid #27AE60 !important;
        }
        
        .stAlert[data-baseweb*="positive"] p {
            color: #1E7E34 !important;
        }
        
        /* Form styling */
        [data-testid="stForm"] {
            background: transparent !important;
        }
        
        /* Base button styling - applies to ALL buttons first */
        button,
        .stButton button,
        [data-testid="stFormSubmitButton"] button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.3s ease !important;
        }
        
        /* Secondary button styling - default for all buttons */
        button:not([kind="primary"]),
        .stButton button:not([kind="primary"]),
        [data-testid="stFormSubmitButton"] button:not([kind="primary"]) {
            background: #FFFFFF !important;
            color: #4A5568 !important;
            border: 2px solid rgba(102, 126, 234, 0.3) !important;
        }
        
        button:not([kind="primary"]):hover,
        .stButton button:not([kind="primary"]):hover,
        [data-testid="stFormSubmitButton"] button:not([kind="primary"]):hover {
            background: rgba(102, 126, 234, 0.05) !important;
            border-color: #667EEA !important;
            color: #667EEA !important;
        }
        
        /* Primary button - coral/salmon gradient (ONLY for buttons with kind="primary") */
        button[kind="primary"],
        .stButton button[kind="primary"],
        [data-testid="stFormSubmitButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #FF6B6B 0%, #E76F51 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3) !important;
        }
        
        button[kind="primary"]:hover,
        .stButton button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
            background: linear-gradient(135deg, #E85555 0%, #D66040 100%) !important;
            box-shadow: 0 6px 16px rgba(255, 107, 107, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Divider/hr styling */
        hr {
            border-color: rgba(102, 126, 234, 0.2) !important;
            margin: 1rem 0 !important;
        }
        </style>
        
        <script>
        // Aggressively force remove all top spacing
        function removeTopSpacing() {
            // Remove spacing from body and html
            document.body.style.paddingTop = '0';
            document.body.style.marginTop = '0';
            document.documentElement.style.paddingTop = '0';
            document.documentElement.style.marginTop = '0';
            
            // Remove spacing from main containers
            const containers = [
                '.stApp',
                '.main',
                '.main .block-container',
                '[data-testid="stAppViewContainer"]',
                '[data-testid="stVerticalBlock"]',
                '[data-testid="element-container"]',
                '[data-testid="stMarkdownContainer"]',
                '.onboarding-container'
            ];
            
            containers.forEach(selector => {
                document.querySelectorAll(selector).forEach(el => {
                    el.style.paddingTop = '0';
                    el.style.marginTop = '0';
                });
            });
            
            // Remove spacing from first elements and nested divs
            const firstElements = document.querySelectorAll('[data-testid="stVerticalBlock"]:first-child, [data-testid="element-container"]:first-child, [data-testid="stMarkdownContainer"]:first-child, [data-testid="stVerticalBlock"] > div, [data-testid="element-container"] > div, [data-testid="stMarkdownContainer"] > div');
            firstElements.forEach(el => {
                el.style.paddingTop = '0';
                el.style.marginTop = '0';
            });
            
            // Remove spacing from onboarding container and its children
            const onboardingContainer = document.querySelector('.onboarding-container');
            if (onboardingContainer) {
                onboardingContainer.style.paddingTop = '0.5rem';
                onboardingContainer.style.marginTop = '0';
                const h1 = onboardingContainer.querySelector('h1');
                if (h1) {
                    h1.style.marginTop = '0';
                    h1.style.paddingTop = '0';
                }
            }
        }
        
        // Run immediately
        removeTopSpacing();
        
        // Run on load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', removeTopSpacing);
        } else {
            removeTopSpacing();
        }
        
        // Run after delays
        setTimeout(removeTopSpacing, 50);
        setTimeout(removeTopSpacing, 100);
        setTimeout(removeTopSpacing, 300);
        setTimeout(removeTopSpacing, 500);
        
        // Monitor for changes
        const observer = new MutationObserver(removeTopSpacing);
        observer.observe(document.body, { childList: true, subtree: true, attributes: true });
        </script>
    """, unsafe_allow_html=True)
    
    # Initialize onboarding step
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    
    st.markdown("<div class='onboarding-container'>", unsafe_allow_html=True)
    
    # Header - with minimal top margin
    st.markdown("<h1 style='text-align: center; color: #FF6B6B; font-family: Poppins, sans-serif; font-weight: 700; margin-top: 0 !important; padding-top: 0 !important; margin-bottom: 0.3rem !important;'>Welcome to Carely! 🎉</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #4A5568; font-family: Inter, sans-serif; margin-top: 0 !important; margin-bottom: 0.5rem !important;'>Let's set up your personalized care experience</p>", unsafe_allow_html=True)
    
    # Step indicator
    show_step_indicator(st.session_state.onboarding_step)
    
    # Display appropriate step
    if st.session_state.onboarding_step == 1:
        show_step_1_profile()
    elif st.session_state.onboarding_step == 2:
        show_step_2_caregiver()
    elif st.session_state.onboarding_step == 3:
        show_step_3_medications_events()
    
    st.markdown("</div>", unsafe_allow_html=True)


def show_step_indicator(current_step: int):
    """Display step progress indicator"""
    steps = [
        ("1", "Profile"),
        ("2", "Caregiver"),
        ("3", "Health Info")
    ]
    
    cols = st.columns(len(steps))
    
    for idx, (col, (num, label)) in enumerate(zip(cols, steps), 1):
        with col:
            if idx < current_step:
                st.markdown(f"<div class='step completed'>✓ {label}</div>", unsafe_allow_html=True)
            elif idx == current_step:
                st.markdown(f"<div class='step active'>{num}. {label}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='step'>{num}. {label}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def show_step_1_profile():
    """Step 1: Basic Profile & Consent"""
    st.markdown("### Step 1: Your Profile")
    st.markdown("Tell us a bit about yourself")
    
    # Get current account
    account = AuthRepository.get_account_by_id(st.session_state.account_id)
    
    # Get existing user if available
    user = None
    if account and account.user_id:
        user = UserCRUD.get_user(account.user_id)
    
    # Pre-fill with existing data
    default_name = user.name if user else account.email.split('@')[0]
    default_timezone = st.session_state.get('timezone', 'America/Chicago')
    
    # Get DOB from preferences if available
    default_dob = date(1950, 1, 1)
    if user and user.preferences:
        try:
            prefs = json.loads(user.preferences) if isinstance(user.preferences, str) else user.preferences
            dob_str = prefs.get('date_of_birth')
            if dob_str:
                default_dob = date.fromisoformat(dob_str)
        except:
            pass
    
    with st.form("profile_form"):
        display_name = st.text_input("Display Name *", value=default_name)
        
        timezone = st.selectbox("Timezone *", 
                               ["America/Chicago", "America/New_York", "America/Los_Angeles", 
                                "America/Denver", "America/Phoenix"],
                               index=0 if default_timezone == "America/Chicago" else 
                                     ["America/Chicago", "America/New_York", "America/Los_Angeles", 
                                      "America/Denver", "America/Phoenix"].index(default_timezone)
                                     if default_timezone in ["America/Chicago", "America/New_York", 
                                                            "America/Los_Angeles", "America/Denver", 
                                                            "America/Phoenix"] else 0)
        
        dob = st.date_input("Date of Birth *", 
                           value=default_dob,
                           min_value=date(1920, 1, 1),
                           max_value=date.today())
        
        # Calculate and display age
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        st.info(f"Age: {age} years")
        
        st.markdown("---")
        
        consent_terms = st.checkbox(
            "I understand that Carely is not a substitute for professional medical advice *",
            value=True
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("← Back to Login"):
                st.session_state.show_onboarding = False
                st.rerun()
        
        with col2:
            submit = st.form_submit_button("Next →", type="primary", use_container_width=True)
        
        if submit:
            if not display_name or not consent_terms:
                st.error("Please fill in all required fields and accept the terms")
                return
            
            # Save profile
            profile_data = {
                'name': display_name,
                'email': account.email,
                'preferences': {
                    'timezone': timezone,
                    'date_of_birth': dob.isoformat(),
                    'age': age,
                    'consent_terms': consent_terms
                }
            }
            
            user = create_or_update_profile(st.session_state.account_id, profile_data)
            
            # Update session state
            st.session_state.user_id = user.id
            st.session_state.user_name = user.name
            st.session_state.timezone = timezone
            
            # Move to next step
            st.session_state.onboarding_step = 2
            st.rerun()


def show_step_2_caregiver():
    """Step 2: Caregiver Contact (Optional)"""
    st.markdown("### Step 2: Caregiver Contact")
    st.markdown("Add a caregiver who can receive alerts and updates (optional)")
    
    # Get Telegram credentials from environment (not shown to user)
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    
    with st.form("caregiver_form"):
        st.markdown("**Caregiver Information**")
        
        caregiver_name = st.text_input("Caregiver Name", placeholder="e.g., John Smith")
        
        contact_channel = st.selectbox("Contact Channel", 
                                      ["Telegram", "Email", "SMS"],
                                      index=0)
        
        if contact_channel == "Telegram":
            if telegram_token and telegram_chat_id:
                st.info("Telegram notifications are configured and ready to use.")
            else:
                st.warning("Telegram is not configured. Please contact your administrator to set up Telegram alerts.")
        else:
            caregiver_contact = st.text_input("Contact Information", 
                                            placeholder="Email or phone number")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.form_submit_button("← Previous"):
                st.session_state.onboarding_step = 1
                st.rerun()
        
        with col2:
            skip = st.form_submit_button("Skip", use_container_width=True)
        
        with col3:
            submit = st.form_submit_button("Next →", type="primary", use_container_width=True)
        
        if skip:
            st.session_state.onboarding_step = 3
            st.rerun()
        
        if submit:
            # Save caregiver if provided
            if caregiver_name:
                # Create caregiver user
                caregiver_email = f"caregiver_{st.session_state.user_id}@carely.local"
                
                caregiver_user = UserCRUD.create_user(
                    name=caregiver_name,
                    email=caregiver_email,
                    user_type="caregiver",
                    preferences={
                        'contact_channel': contact_channel,
                        'telegram_token': telegram_token if contact_channel == "Telegram" else None,
                        'telegram_chat_id': telegram_chat_id if contact_channel == "Telegram" else None
                    }
                )
                
                # Link caregiver to patient
                if caregiver_user:
                    CaregiverPatientCRUD.assign_patient(
                        caregiver_id=caregiver_user.id,
                        patient_id=st.session_state.user_id,
                        relationship="family",
                        notification_preferences={'alerts': True, 'weekly_reports': True}
                    )
                    
                    st.success(f"Caregiver {caregiver_name} added successfully!")
            
            st.session_state.onboarding_step = 3
            st.rerun()


def show_step_3_medications_events():
    """Step 3: Medications & Personal Events (Optional)"""
    st.markdown("### Step 3: Health Information")
    st.markdown("Add your medications and important events (optional)")
    
    # Tabs for medications and events
    tab1, tab2 = st.tabs(["💊 Medications", "📅 Personal Events"])
    
    with tab1:
        show_medication_form()
    
    with tab2:
        show_events_form()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()
    
    with col2:
        if st.button("Skip", use_container_width=True):
            complete_onboarding()
    
    with col3:
        if st.button("Finish ✓", type="primary", use_container_width=True):
            complete_onboarding()


def show_medication_form():
    """Display medication entry form"""
    st.markdown("**Add Medications**")
    
    with st.form("medication_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            med_name = st.text_input("Medication Name *", placeholder="e.g., Lisinopril")
            dose = st.text_input("Dose", placeholder="e.g., 10mg")
            frequency = st.selectbox("Frequency", ["daily", "twice_daily", "weekly", "as_needed"])
        
        with col2:
            reminder_time = st.time_input("Reminder Time *", value=time(9, 0))
            timezone = st.selectbox("Timezone", 
                                   [st.session_state.get('timezone', 'America/Chicago')],
                                   index=0)
            active = st.checkbox("Active", value=True)
        
        instructions = st.text_area("Instructions", placeholder="Optional instructions for taking this medication")
        
        submit = st.form_submit_button("Add Medication", use_container_width=True)
        
        if submit:
            if not med_name or not reminder_time:
                st.error("Please provide medication name and reminder time")
                return
            
            # Verify user_id exists in session
            if 'user_id' not in st.session_state or not st.session_state.user_id:
                st.error("Session error: User ID not found. Please complete Step 1 first.")
                return
            
            # Convert time to schedule times list
            schedule_times = [reminder_time.strftime("%H:%M")]
            if frequency == "twice_daily":
                # Add second time 12 hours later
                second_hour = (reminder_time.hour + 12) % 24
                schedule_times.append(f"{second_hour:02d}:{reminder_time.minute:02d}")
            
            try:
                # Create medication (schedule_times should be a list, not JSON string)
                MedicationCRUD.create_medication(
                    user_id=st.session_state.user_id,
                    name=med_name,
                    dosage=dose,
                    frequency=frequency,
                    schedule_times=schedule_times,
                    instructions=instructions
                )
                
                st.success(f"Medication '{med_name}' added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save medication: {str(e)}")
    
    # Display existing medications
    medications = MedicationCRUD.get_user_medications(st.session_state.user_id)
    if medications:
        st.markdown("**Your Medications:**")
        for med in medications:
            with st.expander(f"💊 {med.name} - {med.dosage}"):
                st.write(f"**Frequency:** {med.frequency}")
                st.write(f"**Schedule:** {med.schedule_times}")
                if med.instructions:
                    st.write(f"**Instructions:** {med.instructions}")
                st.write(f"**Status:** {'Active' if med.active else 'Inactive'}")


def show_events_form():
    """Display personal events entry form"""
    st.markdown("**Add Personal Events**")
    
    with st.form("event_form"):
        title = st.text_input("Event Title *", placeholder="e.g., Doctor's Appointment")
        
        col1, col2 = st.columns(2)
        with col1:
            event_date = st.date_input("Date *", min_value=date.today())
            event_time = st.time_input("Time *", value=time(10, 0))
        
        with col2:
            importance = st.selectbox("Importance", ["low", "medium", "high"], index=1)
            event_type = st.selectbox("Type", 
                                     ["appointment", "medication", "family_event", 
                                      "birthday", "hobby", "health"],
                                     index=0)
        
        notes = st.text_area("Notes", placeholder="Optional notes about this event")
        
        recurrence = st.selectbox("Recurrence", 
                                 ["None", "Daily", "Weekly", "Monthly"],
                                 index=0)
        
        submit = st.form_submit_button("Add Event", use_container_width=True)
        
        if submit:
            if not title:
                st.error("Please provide an event title")
                return
            
            # Verify user_id exists in session
            if 'user_id' not in st.session_state or not st.session_state.user_id:
                st.error("Session error: User ID not found. Please complete Step 1 first.")
                return
            
            # Combine date and time
            event_datetime = datetime.combine(event_date, event_time)
            
            try:
                # Create event
                PersonalEventCRUD.create_event(
                    user_id=st.session_state.user_id,
                    event_type=event_type,
                    title=title,
                    description=notes,
                    event_date=event_datetime,
                    recurring=(recurrence != "None"),
                    importance=importance
                )
                
                st.success(f"Event '{title}' added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save event: {str(e)}")
    
    # Display existing events
    events = PersonalEventCRUD.get_upcoming_events(st.session_state.user_id, days=30)
    if events:
        st.markdown("**Your Upcoming Events:**")
        for event in events[:5]:  # Show first 5
            event_time_str = event.event_date.strftime("%b %d, %Y at %I:%M %p") if event.event_date else "No date"
            with st.expander(f"📅 {event.title} - {event_time_str}"):
                st.write(f"**Type:** {event.event_type}")
                st.write(f"**Importance:** {event.importance}")
                if event.description:
                    st.write(f"**Notes:** {event.description}")


def complete_onboarding():
    """Complete onboarding and redirect to main app"""
    # Mark onboarding as complete
    AuthRepository.mark_onboarding_complete(st.session_state.account_id)
    
    # Clear onboarding flags
    st.session_state.show_onboarding = False
    if 'onboarding_step' in st.session_state:
        del st.session_state.onboarding_step
    
    st.success("🎉 Onboarding complete! Welcome to Carely!")
    st.rerun()
