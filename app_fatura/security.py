from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from db import get_db
from models import User

router = APIRouter()

password_context = CryptContext(schemes=["bcrypt"])


# Password functions.
def hash_password(password: str):
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_context.verify(password, hashed_password)


# JWT:

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
EXPIRE_MINUTES_TOKEN = 30
security = HTTPBearer()

# Create token.
def create_access_token(data: dict):
    # Make a copy of the data to avoid modifying the original
    to_encode = data.copy()
    # Create expiration time -> Current time + X minutes.
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES_TOKEN)
    # Add the expiration claim to the token.
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# JWT validation.
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Extract the token from  authorization: Bearer <token>
    token = credentials.credentials

    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract username from "sub" claim.
        username = payload.get("sub")

        # If username is missing, the token is invalid.
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token- username missing")
        # Returns the username, so the protected routes can use it.
        return username

    # If:
    # - Token is expired,
    # - Signature is wrong,
    # - Token was modified,
    # - Token format is invalid,
    #  We raise this error.
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# Inform FastAPI to expect "Authorization: Bearer <token>".
token_auth_scheme = HTTPBearer()


def get_current_user(token:  HTTPAuthorizationCredentials = Depends(token_auth_scheme), db: Session = Depends(get_db)):

    try:
        # Decode JWT.
        payload = jwt.decode(token.credentials, SECRET_KEY,algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail = "Invalid token. - there is no username")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token. - JWTError")

    # Fetch from the database.
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")

    return user