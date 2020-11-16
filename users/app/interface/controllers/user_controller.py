from dataclasses import asdict
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from app.domain.model.user import User
from app.domain.services import user_service, password_service
from app.domain.services.user_not_found_exception import UserNotFoundException
from app.interface.schemas.user import UserIn

router = APIRouter()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    pwd = credentials.password
    try:
        user = user_service.get_user_by_name(username)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={
                'WWW-Authenticate': 'Basic'
            }
        )
    hash_verified = password_service.verify_password(pwd, user.password_hash)
    if not hash_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Inccorect name or pwd',
            headers={
                'WWW-Authenticate': 'Basic'
            }
        )
    ret = User(**user.serialize)
    return ret


@router.get('/me')
async def me(user: Dict[str, Any] = Depends(get_current_username)):
    return user


# TODO: secure it with bearer
@router.post('/addOne')
async def add_one(user: UserIn):
    user: User = user_service.create_user(user.name, user.password)
    return asdict(user)


@router.get('/getAll')
async def get_all():
    users: List[User] = user_service.get_all_users()
    return list(map(lambda x: asdict(x), users))
