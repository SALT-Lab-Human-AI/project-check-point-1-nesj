"""
Login UI component for Streamlit
"""
import streamlit as st
from datetime import datetime, date
from typing import Optional
import json

from app.auth.auth_repository import AuthRepository, create_or_update_profile
from app.database.crud import UserCRUD


def show_login_page():
    """Display login/signup page"""
    # Apply light wellness-inspired styling matching Overview page
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
        }
        
        /* Hide Streamlit header/toolbar completely */
        header, [data-testid="stHeader"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
        }
        
        /* Remove ALL top padding/margin from every container */
        .main, .main > div, .block-container, div.block-container {
            padding-top: 0.5rem !important;
            margin-top: 0 !important;
            background: transparent !important;
        }
        
        .block-container {
            max-width: 500px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-bottom: 0 !important;
        }
        
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] > section,
        .stApp > header + div {
            padding-top: 0 !important;
            margin-top: 0 !important;
            background: transparent !important;
        }
        
        /* Remove first element top margin */
        .block-container > div:first-child,
        .element-container:first-child,
        [data-testid="stVerticalBlock"] > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        /* Remove gaps between vertical blocks */
        .main [data-testid="stVerticalBlock"] {
            gap: 0.2rem !important;
        }
        
        /* Center horizontal blocks (for logo columns) */
        [data-testid="stHorizontalBlock"] {
            justify-content: center !important;
        }
        
        /* Center the image within its container */
        div[data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
        }
        
        div[data-testid="stImage"] img {
            max-width: 220px !important;
            margin: 0 auto !important;
        }
        
        /* Compact hr with light styling */
        hr {
            margin: 0.4rem 0 !important;
            border-color: rgba(102, 126, 234, 0.2) !important;
        }
        
        /* Tab styling for light theme */
        [data-testid="stTabs"] {
            margin-top: 0 !important;
        }
        
        [data-testid="stTabs"] button {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            color: #4A5568 !important;
        }
        
        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #FF6B6B !important;
            border-bottom-color: #FF6B6B !important;
        }
        
        /* Compact form */
        [data-testid="stForm"] {
            padding: 0.2rem 0 !important;
            background: transparent !important;
        }
        
        /* Headings with dark text for light background */
        h3 {
            margin-top: 0.1rem !important;
            margin-bottom: 0.2rem !important;
            font-size: 1.4rem !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
            color: #2D3436 !important;
        }
        
        /* Paragraphs with readable dark text */
        p {
            margin-bottom: 0.2rem !important;
            color: #4A5568 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Labels with dark text */
        label, .stTextInput label, [data-testid="stTextInput"] label {
            color: #2D3436 !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Input fields with light background and dark text */
        [data-testid="stTextInput"] {
            margin-bottom: 0.3rem !important;
        }
        
        [data-testid="stTextInput"] input {
            background-color: #FFFFFF !important;
            border: 1.5px solid rgba(102, 126, 234, 0.3) !important;
            border-radius: 8px !important;
            color: #2D3436 !important;
            font-family: 'Inter', sans-serif !important;
            padding: 0.6rem 0.8rem !important;
        }
        
        [data-testid="stTextInput"] input:focus {
            border-color: #667EEA !important;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.15) !important;
        }
        
        [data-testid="stTextInput"] input::placeholder {
            color: #A0AEC0 !important;
        }
        
        /* Date input styling */
        [data-testid="stDateInput"] label {
            color: #2D3436 !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stDateInput"] input {
            background-color: #FFFFFF !important;
            border: 1.5px solid rgba(102, 126, 234, 0.3) !important;
            color: #2D3436 !important;
        }
        
        /* Select box styling */
        [data-testid="stSelectbox"] label {
            color: #2D3436 !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stSelectbox"] > div > div {
            background-color: #FFFFFF !important;
            border: 1.5px solid rgba(102, 126, 234, 0.3) !important;
            color: #2D3436 !important;
        }
        
        /* Checkbox styling */
        [data-testid="stCheckbox"] label {
            color: #4A5568 !important;
        }
        
        /* Global font fallback for all text */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: #4A5568 !important;
        }
        
        /* Generic alert base styling */
        [data-testid="stAlert"],
        div[role="alert"],
        .stAlert {
            border-radius: 8px !important;
            padding: 0.8rem 1rem !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Info alert - blue (st.info) */
        .stAlert[data-baseweb*="info"],
        div[data-testid="stNotification"][data-kind="info"],
        [data-testid="stAlert"]:has(svg[data-testid="stInfoIcon"]) {
            background-color: rgba(102, 126, 234, 0.1) !important;
            border-left: 4px solid #667EEA !important;
        }
        
        .stAlert[data-baseweb*="info"] p,
        [data-testid="stAlert"]:has(svg[data-testid="stInfoIcon"]) p {
            color: #2D3436 !important;
        }
        
        /* Error alert - red (st.error) */
        .stAlert[data-baseweb*="negative"],
        .stException,
        div[data-testid="stNotification"][data-kind="error"],
        [data-testid="stAlert"]:has(svg[data-testid="stErrorIcon"]) {
            background-color: rgba(231, 76, 60, 0.1) !important;
            border-left: 4px solid #E74C3C !important;
        }
        
        .stAlert[data-baseweb*="negative"] p,
        [data-testid="stAlert"]:has(svg[data-testid="stErrorIcon"]) p {
            color: #C0392B !important;
        }
        
        /* Warning alert - orange (st.warning) */
        .stAlert[data-baseweb*="warning"],
        div[data-testid="stNotification"][data-kind="warning"],
        [data-testid="stAlert"]:has(svg[data-testid="stWarningIcon"]) {
            background-color: rgba(243, 156, 18, 0.1) !important;
            border-left: 4px solid #F39C12 !important;
        }
        
        .stAlert[data-baseweb*="warning"] p,
        [data-testid="stAlert"]:has(svg[data-testid="stWarningIcon"]) p {
            color: #8B6914 !important;
        }
        
        /* Success alert - green (st.success) */
        .stAlert[data-baseweb*="positive"],
        div[data-testid="stNotification"][data-kind="success"],
        [data-testid="stAlert"]:has(svg[data-testid="stSuccessIcon"]) {
            background-color: rgba(39, 174, 96, 0.1) !important;
            border-left: 4px solid #27AE60 !important;
        }
        
        .stAlert[data-baseweb*="positive"] p,
        [data-testid="stAlert"]:has(svg[data-testid="stSuccessIcon"]) p {
            color: #1E7E34 !important;
        }
        
        /* Primary button - coral/salmon gradient like Overview */
        button[kind="primary"],
        button[kind="formSubmit"],
        [data-testid="stForm"] button[type="submit"],
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #FF6B6B 0%, #E76F51 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            font-family: 'Poppins', sans-serif !important;
            padding: 0.7rem 1.5rem !important;
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        button[kind="primary"]:hover,
        button[kind="formSubmit"]:hover,
        [data-testid="stForm"] button[type="submit"]:hover {
            background: linear-gradient(135deg, #E85555 0%, #D66040 100%) !important;
            box-shadow: 0 6px 16px rgba(255, 107, 107, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Main content area transparent */
        .main {
            background: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Centered Logo using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Logo.png", use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Tabs for login and create account
    tab1, tab2 = st.tabs(["🔐 Log In", "✨ Create Account"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_create_account_form()


def show_login_form():
    """Display login form"""
    st.markdown("### Welcome back!")
    st.markdown("Log in to continue to your dashboard.")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@example.com")
        passcode = st.text_input("Passcode", type="password", placeholder="Enter your passcode")
        
        submit = st.form_submit_button("Log In", use_container_width=True, type="primary")
        
        if submit:
            if not email or not passcode:
                st.error("Please enter both email and passcode")
                return
            
            # Validate credentials
            account = AuthRepository.get_account_by_email(email.lower().strip())
            
            if not account:
                st.error("Invalid email or passcode")
                return
            
            if not AuthRepository.verify_passcode(passcode, account.passcode_hash):
                st.error("Invalid email or passcode")
                return
            
            # Successful login
            session_token = AuthRepository.create_session_token(account.id)
            AuthRepository.update_last_login(account.id)
            
            # Store in session state
            st.session_state.session_token = session_token
            st.session_state.account_id = account.id
            st.session_state.logged_in = True
            
            # Get user profile
            if account.user_id:
                user = UserCRUD.get_user(account.user_id)
                if user:
                    st.session_state.user_id = user.id
                    st.session_state.user_name = user.name
                    
                    # Load timezone from preferences
                    if user.preferences:
                        try:
                            prefs = json.loads(user.preferences) if isinstance(user.preferences, str) else user.preferences
                            st.session_state.timezone = prefs.get('timezone', 'America/Chicago')
                        except:
                            st.session_state.timezone = 'America/Chicago'
                    else:
                        st.session_state.timezone = 'America/Chicago'
            
            # Check if onboarding is complete
            if not account.onboarding_completed:
                st.session_state.show_onboarding = True
            
            st.success(f"Welcome back! Redirecting...")
            st.rerun()


def show_create_account_form():
    """Display account creation form"""
    st.markdown("### Create your account")
    st.markdown("Join Carely to start your personalized care journey.")
    
    with st.form("create_account_form"):
        email = st.text_input("Email *", placeholder="your.email@example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            display_name = st.text_input("Display Name", placeholder="Optional (uses email prefix)")
        with col2:
            timezone = st.selectbox("Timezone *", 
                                   ["America/Chicago", "America/New_York", "America/Los_Angeles", 
                                    "America/Denver", "America/Phoenix"],
                                   index=0)
        
        # Date of birth
        dob = st.date_input("Date of Birth *", 
                           min_value=date(1920, 1, 1),
                           max_value=date.today(),
                           value=date(1950, 1, 1))
        
        # Calculate age
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        st.info(f"Age: {age} years")
        
        passcode = st.text_input("Passcode *", type="password", 
                                placeholder="Create a secure passcode")
        passcode_confirm = st.text_input("Confirm Passcode *", type="password",
                                        placeholder="Re-enter your passcode")
        
        st.markdown("---")
        
        # Consent checkboxes
        consent_terms = st.checkbox(
            "I agree to the Terms of Service and understand that Carely is not a substitute for medical advice *",
            value=False
        )
        
        consent_metrics = st.checkbox(
            "I consent to anonymous usage metrics to help improve the service (optional)",
            value=True
        )
        
        st.markdown("*Required fields")
        
        submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
        
        if submit:
            # Validation
            if not email or not passcode:
                st.error("Please fill in all required fields")
                return
            
            if not consent_terms:
                st.error("You must agree to the Terms of Service to continue")
                return
            
            if passcode != passcode_confirm:
                st.error("Passcodes do not match")
                return
            
            if len(passcode) < 6:
                st.error("Passcode must be at least 6 characters")
                return
            
            # Create account
            email_clean = email.lower().strip()
            
            # Check if account exists
            existing = AuthRepository.get_account_by_email(email_clean)
            if existing:
                st.error("An account with this email already exists")
                return
            
            # Create account
            account = AuthRepository.create_account(email_clean, passcode, "demo")
            
            if not account:
                st.error("Failed to create account. Please try again.")
                return
            
            # Create user profile
            profile_data = {
                'name': display_name or email_clean.split('@')[0],
                'email': email_clean,
                'preferences': {
                    'timezone': timezone,
                    'date_of_birth': dob.isoformat(),
                    'age': age,
                    'consent_terms': consent_terms,
                    'consent_metrics': consent_metrics
                }
            }
            
            user = create_or_update_profile(account.id, profile_data)
            
            # Create session
            session_token = AuthRepository.create_session_token(account.id)
            
            # Store in session state
            st.session_state.session_token = session_token
            st.session_state.account_id = account.id
            st.session_state.user_id = user.id
            st.session_state.user_name = user.name
            st.session_state.timezone = timezone
            st.session_state.logged_in = True
            st.session_state.show_onboarding = True
            
            st.success("Account created successfully! Redirecting to onboarding...")
            st.rerun()


def check_authentication():
    """
    Check if user is authenticated
    Returns True if authenticated, False otherwise
    """
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'session_token' not in st.session_state:
        return False
    
    # Validate session token
    account_id = AuthRepository.validate_session_token(st.session_state.session_token)
    
    if not account_id:
        # Invalid token, clear session
        clear_session()
        return False
    
    # Ensure account_id is set
    if 'account_id' not in st.session_state:
        st.session_state.account_id = account_id
    
    return True


def clear_session():
    """Clear session state and log out"""
    if 'session_token' in st.session_state:
        AuthRepository.invalidate_session_token(st.session_state.session_token)
    
    # Clear all auth-related session state
    keys_to_clear = ['session_token', 'account_id', 'user_id', 'user_name', 
                     'logged_in', 'show_onboarding', 'timezone']
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def show_logout_button():
    """Display logout button in sidebar with matching purple gradient styling"""
    # Add CSS for logout button to match Chat section buttons
    st.sidebar.markdown("""
        <style>
        /* Style logout button with purple gradient matching Quick Actions */
        div[data-testid="stSidebar"] button[kind="secondary"] {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2) !important;
        }
        
        div[data-testid="stSidebar"] button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #5568D3 0%, #654A8F 100%) !important;
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3) !important;
            transform: translateY(-2px) !important;
        }
        
        div[data-testid="stSidebar"] button[kind="secondary"]:active {
            transform: translateY(0px) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Log Out", use_container_width=True):
        clear_session()
        st.rerun()
