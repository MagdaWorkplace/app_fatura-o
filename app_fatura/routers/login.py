from fastapi import APIRouter, HTTPException, Depends
from models import RequestLogin, User
from security import verify_password, create_access_token
from db import get_db
from sqlalchemy.orm import Session

# Create a router for the login routes.
router = APIRouter()


# Post - login route.
# Receive JSON with the username and password.
@router.post("/login")
# The db_ Session = Depends(get_db) -> tells the FastAPI to open a database session from this request.
def login(request_login: RequestLogin, db: Session = Depends(get_db)):
    # Checks if username exists in the database.
    user = db.query(User).filter(User.username == request_login.username).first()
    if user:
        # Verify the password against the hashed version stored in the database.
        if verify_password(request_login.password, user.hashed_password):
            # Create the JWT token.
            access_token = create_access_token({"sub": request_login.username})

            # Returns the access token used by the protected routes.
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            # Wrong password.
            raise HTTPException(status_code=400, detail="Wrong password!")
    else:
        # User doesn't exist.
        raise HTTPException(status_code=400, detail="User doesn't exist!")
