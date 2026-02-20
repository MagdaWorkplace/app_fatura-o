from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
# Create a router for the login routes.
router = APIRouter()

password_context = CryptContext(schemes=["bcrypt"])

# Temporary database for testing.
users_dic = {"Alice": password_context.hash("123"), "Rute": password_context.hash("456")}

# Model fot JSON body of the post request.
class RequestLogin(BaseModel):
    username: str
    password: str

# Post - login route.
# Receive JSON with the username and password.
@router.post("/login")
def login(request_login: RequestLogin):
    # Checks if username exists in the database.
    if request_login.username in users_dic.keys():
        # If exists, checks if the password is correct - Compare with the hash version.
        hashed_password = users_dic[request_login.username]
        password_to_check = request_login.password
        if password_context.verify(password_to_check, hashed_password):
            return {"status": "Logged in."}
        else:
            raise HTTPException(status_code=400, detail="Wrong password!")
    else:
        raise HTTPException(status_code=400, detail="User doesn't exist!")
