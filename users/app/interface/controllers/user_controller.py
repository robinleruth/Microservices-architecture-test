from dataclasses import asdict
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from tcommon.oauth_implem import OauthImplem

from app.domain.model.user import User
from app.domain.services import user_service, password_service
from app.domain.services.user_not_found_exception import UserNotFoundException
from app.infrastructure.config import app_config
from app.infrastructure.log import logger
from app.interface.schemas.user import UserIn, UpdateScope

router = APIRouter()

security = HTTPBasic()

oauth_implem = OauthImplem(scopes=app_config.SCOPES, client_id=app_config.CLIENT_ID)


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


@router.post('/addOne')
async def add_one(user: UserIn):
    logger.info(f'Create a user : {user}')
    user: User = user_service.create_user(user.name, user.password, user.scopes)
    return asdict(user)


@router.get('/getAll')
async def get_all(user_auth=Security(oauth_implem.get_user_implicit(), scopes=['all'])):
    users: List[User] = user_service.get_all_users()
    return list(map(lambda x: asdict(x), users))


@router.put('/updateScopes')
async def update_scopes(update_scope: UpdateScope, user_auth=Security(oauth_implem.get_user_implicit(), scopes=['me'])):
    return user_service.update_scope(user_auth.nickname, update_scope.scopes)
