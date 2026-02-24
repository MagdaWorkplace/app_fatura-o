from fastapi import APIRouter, HTTPException
from models import RequestLogin
from passlib.context import CryptContext
from security import verify_password, create_access_token
from db import users_dic
# Create a router for the login routes.
router = APIRouter()

# Post - login route.
# Receive JSON with the username and password.
@router.post("/login")
def login(request_login: RequestLogin):
    # Checks if username exists in the database.
    if request_login.username in users_dic.keys():
        # If exists, checks if the password is correct - Compare with the hash version.
        hashed_password = users_dic[request_login.username]
        password_to_check = request_login.password
        if verify_password(password_to_check, hashed_password):
            access_token = create_access_token({"sub": request_login.username})

            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail="Wrong password!")
    else:
        raise HTTPException(status_code=400, detail="User doesn't exist!")

