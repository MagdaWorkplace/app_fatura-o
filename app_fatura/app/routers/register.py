from fastapi import APIRouter, HTTPException
from models import RequestRegister
from passlib.context import CryptContext
from security import hash_password
from db import users_dic
# Create a router for the register routes.
router = APIRouter()

# Post - register route.
# Receive JSON with the username and password.
@router.post("/register")
def register(request_register: RequestRegister):
    # Checks if the username already exists.
    if request_register.username in users_dic:
        raise HTTPException(status_code=409, detail= "Username already exists")

    # Hash password before storing.
    # If username doesn't exist, add it to the dictionary.
    users_dic[request_register.username] = hash_password(request_register.password)
    return {"status": "Successfully added!"}
