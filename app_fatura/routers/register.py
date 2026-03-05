from fastapi import APIRouter, HTTPException, Depends
from models import RequestRegister, User
from security import hash_password
from db import get_db
from sqlalchemy.orm import Session


# Create a router for the register routes.
router = APIRouter()


# Post - register route.
# Receive JSON with the username and password.
@router.post("/register")
# The db_ Session = Depends(get_db) -> tells the FastAPI to open a database session from this request.
def register(request_register: RequestRegister, db: Session = Depends(get_db)):
    # Checks if the username already exists in the database.
    existing_user = db.query(User).filter(User.username == request_register.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    # Hash plaint password before storing it.
    hashed_password = hash_password(request_register.password)
    # If username doesn't exist, add it to the dictionary.
    # Create a new User instance.
    new_user = User(username=request_register.username, hashed_password=hashed_password)
    # Add it to the database.
    db.add(new_user)
    # Commit the session-
    db.commit()
    # Refresh the object from DB.
    db.refresh(new_user)

    return {"status": "Successfully added!"}
