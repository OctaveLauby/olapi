from fastapi import APIRouter, Depends

from olapi.dependencies import current_user
from olapi.models.user import UserModel

router = APIRouter()


@router.get("/hello")
def hello(user: UserModel = Depends(current_user)) -> dict[str, str]:
    return {"message": f"Hello {user.username} !"}
