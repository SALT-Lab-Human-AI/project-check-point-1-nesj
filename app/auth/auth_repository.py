"""
Repository layer for authentication operations
"""
import bcrypt
import hmac
import hashlib
import secrets
import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlmodel import Session, select

from app.database.models import get_session, User
from app.auth.auth_models import Account, SessionToken
from utils.timezone_utils import now_central


class AuthRepository:
    """Repository for authentication operations"""
    
    SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "carely-session-secret-change-in-production")
    TOKEN_EXPIRY_HOURS = 24
    
    @staticmethod
    def hash_passcode(passcode: str) -> str:
        """Hash a passcode using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(passcode.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_passcode(passcode: str, hashed: str) -> bool:
        """Verify a passcode against its hash"""
        return bcrypt.checkpw(passcode.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def generate_session_token(account_id: int) -> str:
        """Generate an HMAC-signed session token"""
        random_part = secrets.token_urlsafe(32)
        data = f"{account_id}:{random_part}:{now_central().timestamp()}"
        signature = hmac.new(
            AuthRepository.SECRET_KEY.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{data}:{signature}"
    
    @staticmethod
    def verify_session_token(token: str) -> Optional[int]:
        """Verify a session token and return account_id if valid"""
        try:
            parts = token.split(':')
            if len(parts) != 4:
                return None
            
            account_id, random_part, timestamp, signature = parts
            data = f"{account_id}:{random_part}:{timestamp}"
            
            expected_signature = hmac.new(
                AuthRepository.SECRET_KEY.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return None
            
            return int(account_id)
        except:
            return None
    
    @staticmethod
    def create_account(email: str, passcode: str, provider: str = "demo", 
                      user_id: Optional[int] = None) -> Optional[Account]:
        """Create a new account"""
        with get_session() as session:
            # Check if email already exists
            existing = session.exec(
                select(Account).where(Account.email == email)
            ).first()
            
            if existing:
                return None
            
            passcode_hash = AuthRepository.hash_passcode(passcode)
            
            account = Account(
                email=email,
                passcode_hash=passcode_hash,
                auth_provider=provider,
                user_id=user_id,
                created_at=now_central()
            )
            
            session.add(account)
            session.commit()
            session.refresh(account)
            return account
    
    @staticmethod
    def get_account_by_email(email: str) -> Optional[Account]:
        """Get account by email"""
        with get_session() as session:
            return session.exec(
                select(Account).where(Account.email == email)
            ).first()
    
    @staticmethod
    def get_account_by_id(account_id: int) -> Optional[Account]:
        """Get account by ID"""
        with get_session() as session:
            return session.exec(
                select(Account).where(Account.id == account_id)
            ).first()
    
    @staticmethod
    def update_last_login(account_id: int):
        """Update last login timestamp"""
        with get_session() as session:
            account = session.exec(
                select(Account).where(Account.id == account_id)
            ).first()
            
            if account:
                account.last_login = now_central()
                session.add(account)
                session.commit()
    
    @staticmethod
    def mark_onboarding_complete(account_id: int):
        """Mark onboarding as completed"""
        with get_session() as session:
            account = session.exec(
                select(Account).where(Account.id == account_id)
            ).first()
            
            if account:
                account.onboarding_completed = True
                session.add(account)
                session.commit()
    
    @staticmethod
    def create_session_token(account_id: int) -> str:
        """Create and store a session token"""
        token = AuthRepository.generate_session_token(account_id)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        with get_session() as session:
            session_token = SessionToken(
                account_id=account_id,
                token_hash=token_hash,
                issued_at=now_central(),
                expires_at=now_central() + timedelta(hours=AuthRepository.TOKEN_EXPIRY_HOURS)
            )
            
            session.add(session_token)
            session.commit()
        
        return token
    
    @staticmethod
    def validate_session_token(token: str) -> Optional[int]:
        """Validate a session token and return account_id if valid"""
        account_id = AuthRepository.verify_session_token(token)
        
        if not account_id:
            return None
        
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        with get_session() as session:
            db_token = session.exec(
                select(SessionToken).where(
                    SessionToken.account_id == account_id,
                    SessionToken.token_hash == token_hash,
                    SessionToken.is_valid == True
                )
            ).first()
            
            if not db_token:
                return None
            
            # Check expiry - make database datetime timezone-aware for comparison
            from utils.timezone_utils import make_aware_central
            expires_at_aware = make_aware_central(db_token.expires_at)
            if expires_at_aware < now_central():
                db_token.is_valid = False
                session.add(db_token)
                session.commit()
                return None
            
            return account_id
    
    @staticmethod
    def invalidate_session_token(token: str):
        """Invalidate a session token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        with get_session() as session:
            db_token = session.exec(
                select(SessionToken).where(
                    SessionToken.token_hash == token_hash
                )
            ).first()
            
            if db_token:
                db_token.is_valid = False
                session.add(db_token)
                session.commit()


def create_or_update_profile(account_id: int, profile_data: Dict[str, Any]) -> User:
    """Create or update user profile linked to account"""
    from app.database.crud import UserCRUD
    
    with get_session() as session:
        # Get account
        account = session.exec(
            select(Account).where(Account.id == account_id)
        ).first()
        
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Check if user already exists
        if account.user_id:
            # Update existing user
            user = UserCRUD.get_user(account.user_id)
            if user:
                # Update fields
                if 'name' in profile_data:
                    user.name = profile_data['name']
                if 'email' in profile_data:
                    user.email = profile_data['email']
                if 'phone' in profile_data:
                    user.phone = profile_data['phone']
                if 'preferences' in profile_data:
                    # Convert dict to JSON string for storage
                    user.preferences = json.dumps(profile_data['preferences']) if isinstance(profile_data['preferences'], dict) else profile_data['preferences']
                
                with get_session() as sess:
                    sess.add(user)
                    sess.commit()
                    sess.refresh(user)
                
                return user
        
        # Create new user
        prefs = profile_data.get('preferences', {})
        # Convert dict to JSON string for storage
        prefs_json = json.dumps(prefs) if isinstance(prefs, dict) else prefs
        
        user = UserCRUD.create_user(
            name=profile_data.get('name', account.email.split('@')[0]),
            email=profile_data.get('email', account.email),
            phone=profile_data.get('phone'),
            preferences=prefs_json
        )
        
        # Link user to account
        account.user_id = user.id
        session.add(account)
        session.commit()
        
        return user
