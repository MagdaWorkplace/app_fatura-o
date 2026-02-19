from fastapi import APIRouter
from pydantic import BaseModel

# Criar um router para as rotas do login
router = APIRouter()

# Temporary database for testing.
users = {"Alice": "123", "Rute": "456"}

# Model fot JSON body of the post request.
class RequestLogin(BaseModel):
    username: str
    password: str

# Post - login route.
# Receive JSON with the username and password.
@router.post("/login")
def login(request_login: RequestLogin):
    # Checks if username exists in the database.
    if request_login.username in users.keys():
        # If exists, checks if the password is correct.
        if users[request_login.username] == request_login.password:
            return {"status": "success"}
        else:
            return {"status": "Wrong password"}
    else:
        return {"status": "User doesn't exist"}
