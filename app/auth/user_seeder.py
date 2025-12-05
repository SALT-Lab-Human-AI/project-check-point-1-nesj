"""
Seed existing test users into the new authentication system
"""
from app.database.crud import UserCRUD
from app.auth.auth_repository import AuthRepository
from utils.timezone_utils import now_central


DEFAULT_DEMO_PASSCODE = "carely-demo"


def seed_existing_users():
    """
    Migrate existing hardcoded users to the new account system
    Creates Account records for existing User records
    """
    print("Seeding existing users into authentication system...")
    
    # Get all existing users
    existing_users = UserCRUD.get_all_users()
    
    for user in existing_users:
        # Check if account already exists for this user
        if user.email:
            account = AuthRepository.get_account_by_email(user.email)
            
            if not account:
                # Create account for this user
                print(f"Creating account for existing user: {user.name} ({user.email})")
                
                account = AuthRepository.create_account(
                    email=user.email,
                    passcode=DEFAULT_DEMO_PASSCODE,
                    provider="demo_seeded",
                    user_id=user.id
                )
                
                if account:
                    # Mark onboarding as complete since they already have data
                    AuthRepository.mark_onboarding_complete(account.id)
                    print(f"  ✓ Account created (ID: {account.id})")
                else:
                    print(f"  ✗ Failed to create account")
    
    print("✓ User seeding complete")


def ensure_test_users_exist():
    """
    Ensure test users exist in the system
    Call this on app startup
    """
    try:
        seed_existing_users()
    except Exception as e:
        print(f"Warning: Could not seed users: {e}")
