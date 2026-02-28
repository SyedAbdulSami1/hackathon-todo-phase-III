import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select
from db import engine, create_db_and_tables
from models import User
from dependencies.auth import get_password_hash, verify_password

def test_auth_logic():
    print("--- AUTH DEBUG TEST ---")
    print(f"Time: {datetime.now()}")
    
    # 1. Test Hashing
    print("\n1. Testing Hashing...")
    try:
        test_pass = "password123"
        hashed = get_password_hash(test_pass)
        print(f"Hashed: {hashed[:20]}...")
        verified = verify_password(test_pass, hashed)
        print(f"Verified: {verified}")
    except Exception as e:
        print(f"HASH ERROR: {e}")

    # 2. Test DB Connection
    print("\n2. Testing DB Connection...")
    try:
        create_db_and_tables()
        with Session(engine) as session:
            # Try to select
            statement = select(User).limit(1)
            user = session.exec(statement).first()
            print(f"DB Connect OK. Found user: {user.username if user else 'None'}")
    except Exception as e:
        print(f"DB ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_logic()
