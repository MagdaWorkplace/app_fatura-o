from fastapi import APIRouter, Depends
from security import get_current_user

router = APIRouter()


# Protected route after being authenticated.
@router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}. You are authenticated!"}
