from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Create a router for the register routes.
router = APIRouter()

# Temporary database for testing.
users_dic = {"Mimi": 123}

# Model fot JSON body of the post request.
class RequestRegister(BaseModel):
    username:str
    password:str

# Post - register route.
# Receive JSON with the username and password.
@router.post("/register")
def register(request_register: RequestRegister):
    # Checks if the username already exists.
    if request_register.username in users_dic:
        raise HTTPException(status_code=409, detail= "Username already exists")

    # If username doesn't exist, add it to the dictionary.
    users_dic[request_register.username] = request_register.password
    return {"status": "Successfully added!"}