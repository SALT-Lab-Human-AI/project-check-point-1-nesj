"""
Authentication models for user accounts and sessions
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from utils.timezone_utils import now_central


class Account(SQLModel, table=True):
    """User account for authentication"""
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    passcode_hash: str  # bcrypt hash
    auth_provider: str = Field(default="demo")  # demo, oauth, etc.
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=now_central)
    last_login: Optional[datetime] = None
    onboarding_completed: bool = Field(default=False)
    
    # Link to existing User model
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class SessionToken(SQLModel, table=True):
    """Session tokens for authenticated users"""
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="account.id")
    token_hash: str  # HMAC-signed token hash
    issued_at: datetime = Field(default_factory=now_central)
    expires_at: datetime
    is_valid: bool = Field(default=True)
