import logging
from dataclasses import asdict
from typing import Dict, Any, List

import requests
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2
from starlette import status

from app.domain.model.user import User
from app.domain.services import user_service, password_service
from app.domain.services.user_not_found_exception import UserNotFoundException
from app.infrastructure.config import app_config
from app.interface.schemas.user import UserIn

router = APIRouter()

security = HTTPBasic()


# TODO: Remove everything that will be in the common library
class UnauthorizedException(Exception):
    pass


logger = logging.getLogger(__name__)


def get_user_info_by_token(token: str) -> {}:
    url = app_config.TOKEN_SERVICE_URL + app_config.TOKEN_INFO
    logger.info(f"GET {url}")
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        if r.status_code == 401:
            raise UnauthorizedException(str(r.json()))
        else:
            raise Exception(f'An error occured while getting {url} : status code {r.status_code}, message {r.json()}')
    return r.json()


url = app_config.TOKEN_SERVICE_URL + app_config.SIGN_IN_PAGE
oauth2_scheme: OAuth2 = OAuth2(
    flows=OAuthFlows(implicit=OAuthFlowImplicit(authorizationUrl=url + f'?client_id={app_config.CLIENT_ID}',
                                                scopes={'test': 'test'})))


def get_user_implicit(token: str = Security(oauth2_scheme)):
    try:
        token = token.split('Bearer ')[1]
    except:
        pass
    try:
        user = get_user_info_by_token(token)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Error authorizing {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Could not authenticate')
    return user


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
async def add_one(user: UserIn, user_auth=Depends(get_user_implicit)):
    user: User = user_service.create_user(user.name, user.password)
    return asdict(user)


@router.get('/getAll')
async def get_all():
    users: List[User] = user_service.get_all_users()
    return list(map(lambda x: asdict(x), users))
