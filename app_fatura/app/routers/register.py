from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from passlib.context import CryptContext


# Create a router for the register routes.
router = APIRouter()

# Password hashing context.
password_context = CryptContext(schemes=["bcrypt"])

# Temporary database for testing.
users_dic = {}


# Model fot JSON body of the post request.
class RequestRegister(BaseModel):
    username:str
    password:str = Field(max_length=72, description="The password need to be 72 charcters or less.")

# Post - register route.
# Receive JSON with the username and password.
@router.post("/register")
def register(request_register: RequestRegister):
    # Checks if the username already exists.
    if request_register.username in users_dic:
        raise HTTPException(status_code=409, detail= "Username already exists")

    # Hash password before storing.
    hashed_password = password_context.hash(request_register.password[:72])
    # If username doesn't exist, add it to the dictionary.
    users_dic[request_register.username] = hashed_password
    return {"status": "Successfully added!"}
