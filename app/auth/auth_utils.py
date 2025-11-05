import hashlib
import secrets
from typing import Optional
from app.database.models import User, get_session
from sqlmodel import select

def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-SHA256 with salt
    Returns: salt$hash format for storage
    """
    # Generate a random salt
    salt = secrets.token_hex(32)
    # Use PBKDF2 with 100000 iterations (OWASP recommended minimum)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${pwd_hash.hex()}"

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its salted hash"""
    try:
        # Handle legacy SHA-256 hashes (backwards compatibility)
        if '$' not in password_hash:
            # Legacy format - still verify but should be migrated
            return hashlib.sha256(password.encode()).hexdigest() == password_hash
        
        # New format: salt$hash
        salt, stored_hash = password_hash.split('$')
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return pwd_hash.hex() == stored_hash
    except Exception:
        return False

def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    with get_session() as session:
        query = select(User).where(User.email == email)
        user = session.exec(query).first()
        
        if user and user.password_hash and verify_password(password, user.password_hash):
            return user
        return None

def generate_session_token() -> str:
    """Generate a random session token"""
    return secrets.token_urlsafe(32)

def check_permission(user: User, required_role: str) -> bool:
    """Check if user has required permission"""
    role_hierarchy = {
        "patient": 0,
        "caregiver": 1,
        "admin": 2
    }
    
    user_level = role_hierarchy.get(user.user_type, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
