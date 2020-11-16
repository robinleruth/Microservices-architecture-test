import logging
from dataclasses import asdict
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from starlette import status

from app.domain.model.credentials import Credentials
from app.domain.model.token import Token
from app.domain.model.user import User
from app.domain.model.user_not_found import UserNotFound
from app.domain.services.token.bean import get_token_service
from app.domain.services.token.token_service import TokenService
from app.infrastructure.config import app_config
from app.infrastructure.connector.user_service_connection_error import UserServiceConnectionError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger(__name__)


async def get_current_user(token: str = Depends(oauth2_scheme),
                           token_service: TokenService = Depends(get_token_service)):
    try:
        token_data = token_service.decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = token_service.get_by_token(token)
    except (UserNotFound, UserServiceConnectionError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not found {token_data.username}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get('/me')
async def get(user: User = Depends(get_current_user)):
    return asdict(user)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 token_service: TokenService = Depends(get_token_service)):
    credentials: Credentials = Credentials(form_data.username, form_data.password)
    logger.info(f'Creating token for {form_data.username}')
    access_token_expires = timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    try:
        access_token = token_service.create_access_token(form_data.username, credentials=credentials,
                                                         expires_delta=access_token_expires)
    except (UserNotFound, UserServiceConnectionError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": access_token, "token_type": "bearer"}
