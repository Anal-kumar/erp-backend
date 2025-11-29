from datetime import datetime, timedelta
from typing import Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.modules.users.models import User
import secrets

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token blacklist (use Redis in production)
token_blacklist = set()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, user_login_id: str, password: str):
    user = db.query(User).filter(User.user_login_id == user_login_id).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, int(expire.timestamp())

def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Create refresh token with longer expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # 7 days for refresh token
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def blacklist_token(token: str):
    """Add token to blacklist"""
    token_blacklist.add(token)

def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    return token in token_blacklist

def validate_password_strength(password: str) -> bool:
    """
    Validate password strength
    Requirements: 8+ chars, upper, lower, digit, special char
    """
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    return has_upper and has_lower and has_digit and has_special

def sanitize_input(input_string: str) -> str:
    """Sanitize user input to prevent XSS"""
    dangerous_chars = ['<', '>', '"', "'", '&', ';']
    sanitized = input_string
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()

def generate_csrf_token() -> str:
    """Generate CSRF token"""
    return secrets.token_urlsafe(32)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    token = credentials.credentials
    
    # Check if token is blacklisted
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_login_id: str = payload.get("sub")
        user_role: str = payload.get("role")
        if user_login_id is None or user_role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

    user = db.query(User).filter(User.user_login_id == user_login_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "user": user,
        "role": user_role,
    }
