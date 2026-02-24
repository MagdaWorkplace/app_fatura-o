from fastapi import APIRouter, Depends
from security import verify_token

router = APIRouter()


# Protected route after being authenticated.
@router.get("/protected")
def protected_route(current_user: str = Depends(verify_token)):
    return {"message": f"Hello {current_user}. You are authenticated!"}
