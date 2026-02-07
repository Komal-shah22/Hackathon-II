import os
import uuid
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select
from pydantic import EmailStr

from db import get_session
from models import User
from schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    AuthResponse,
    MessageResponse,
    ErrorResponse,
)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Security
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    # Fallback secret only for development - this should be set in production
    JWT_SECRET = os.getenv("DEV_JWT_SECRET", "90df3dfaec15056dd3902590eaf1bd5d0787ac40c0f6aa93649cf7b74d54df32")
    if JWT_SECRET == "90df3dfaec15056dd3902590eaf1bd5d0787ac40c0f6aa93649cf7b74d54df32":
        print("WARNING: Using default JWT secret. This should be changed in production!")
        # For HuggingFace Spaces, we might have a different environment variable
        HF_JWT_SECRET = os.getenv("HF_JWT_SECRET")
        if HF_JWT_SECRET:
            JWT_SECRET = HF_JWT_SECRET

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password, ensuring it doesn't exceed bcrypt's 72-character limit"""
    # Bcrypt only uses the first 72 bytes, so we truncate if necessary
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes but decode back to string for hashing
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user account.

    Args:
        user_data: User registration data (email, password, optional name)
        session: Database session dependency

    Returns:
        AuthResponse with user info and JWT token

    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        # Validate input data
        if not user_data.email or '@' not in user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email address"
            )

        if len(user_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )

        # Check if email already exists
        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create user
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email.lower().strip(),  # Normalize email
            name=user_data.name.strip() if user_data.name else None,
            password_hash=get_password_hash(user_data.password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create token
        token = create_access_token(data={"sub": user.id, "email": user.email})

        return AuthResponse(user=UserResponse.from_orm(user), token=token)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as ve:
        # Handle validation errors from Pydantic
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(ve)}"
        )
    except Exception as e:
        # Log the error for debugging (only in non-production environments)
        import os
        if os.getenv("ENVIRONMENT") != "production":
            print(f"Signup error: {str(e)}")
            import traceback
            traceback.print_exc()

        # Raise a generic server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signup"
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate a user and return a JWT token.

    Args:
        credentials: User login credentials (email, password)
        session: Database session dependency

    Returns:
        AuthResponse with user info and JWT token

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        # Validate input data
        if not credentials.email or '@' not in credentials.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email address"
            )

        if not credentials.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required"
            )

        # Find user by email
        user = session.exec(select(User).where(User.email == credentials.email.lower().strip())).first()

        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create token
        token = create_access_token(data={"sub": user.id, "email": user.email})

        return AuthResponse(user=UserResponse.from_orm(user), token=token)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as ve:
        # Handle validation errors from Pydantic
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(ve)}"
        )
    except Exception as e:
        # Log the error for debugging (only in non-production environments)
        import os
        if os.getenv("ENVIRONMENT") != "production":
            print(f"Signin error: {str(e)}")
            import traceback
            traceback.print_exc()

        # Raise a generic server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signin"
        )


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify JWT token and extract payload.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        Token payload with user_id and email

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )

        return {"user_id": user_id, "email": email}

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


async def get_current_user_id(
    payload: dict = Depends(verify_token)
) -> str:
    """
    Dependency to get current user ID from JWT.

    Args:
        payload: Verified token payload

    Returns:
        user_id string
    """
    return payload["user_id"]


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get the current authenticated user's profile.

    Args:
        current_user_id: User ID from JWT token
        session: Database session dependency

    Returns:
        User profile information

    Raises:
        HTTPException: If user not found
    """
    user = session.get(User, current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.from_orm(user)


@router.post("/logout", response_model=MessageResponse)
async def logout():
    """
    Logout user (client-side token removal).

    Note: JWT tokens are stateless, so this is a client-side operation.
    The client should remove the token from storage.

    Returns:
        Success message
    """
    return MessageResponse(message="Logged out successfully. Please remove the token from client storage.")
