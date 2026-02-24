from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

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
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES_TOKEN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

# JWT validation.
def verify_token (credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")