from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from models import User, UserCreate, UserResponse, UserLogin, Token, AuthResponse
from db import get_session
from dependencies.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

@router.post("/register", response_model=AuthResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user and return user with access token"""
    print(f"DEBUG: Registering user: {user.username}, {user.email}")
    try:
        # Check if user already exists
        statement = select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
        print(f"DEBUG: Checking for existing user...")
        existing_user = session.exec(statement).first()

        if existing_user:
            print(f"DEBUG: User already exists: {user.username}")
            raise HTTPException(
                status_code=400,
                detail="User already registered"
            )

        # Create new user
        print(f"DEBUG: Hashing password...")
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        print(f"DEBUG: Adding user to session...")
        session.add(db_user)
        print(f"DEBUG: Committing session...")
        session.commit()
        print(f"DEBUG: Refreshing user...")
        session.refresh(db_user)
        print(f"DEBUG: User registered successfully: {db_user.id}")

        # Generate token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )

        return {
            "user": db_user,
            "token": token,
            "token_type": "bearer"
        }
    except HTTPException as e:
        print(f"DEBUG: HTTP error during registration: {e.detail}")
        raise e
    except Exception as e:
        print(f"DEBUG: Unexpected error during registration: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=AuthResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Login user and return access token and user info"""
    print(f"DEBUG: Attempting login for user: {form_data.username}")
    try:
        user = authenticate_user(session, form_data.username, form_data.password)
        print(f"DEBUG: User {form_data.username} authenticated successfully")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        print(f"DEBUG: Token created for {form_data.username}")

        return {
            "user": user,
            "token": token,
            "token_type": "bearer"
        }
    except HTTPException as e:
        print(f"DEBUG: HTTP Error during login: {e.detail}")
        raise e
    except Exception as e:
        print(f"DEBUG: Unexpected error during login: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user
