from fastapi import APIRouter, Depends

from olapi.deps import current_user
from olapi.models.user import User

router = APIRouter()


@router.get("/hello")
def hello(user: User = Depends(current_user)) -> dict[str, str]:
    return {"message": f"Hello {user.username} !"}
