from fastapi import APIRouter, Depends

from olapi.auth import get_user
from olapi.models.user import UserModel

router = APIRouter()


@router.get("/hello")
def hello(user: UserModel = Depends(get_user)) -> dict[str, str]:
    return {"message": f"Hello {user.username} !"}
