import os
import urllib.parse as urlparse
from dataclasses import asdict
from datetime import timedelta
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Form, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from jose import JWTError
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.domain.model.credentials import Credentials
from app.domain.model.scope_not_allowed import ScopeNotAllowedException
from app.domain.model.token import Token
from app.domain.model.user import User
from app.domain.model.user_not_found import UserNotFound
from app.domain.services.client_id import client_id_service
from app.domain.services.token.bean import get_token_service
from app.domain.services.token.token_service import TokenService
from app.infrastructure.config import app_config
from app.infrastructure.connector.user_service_connection_error import UserServiceConnectionError
from app.infrastructure.log import logger

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token_controller/token",
                                     scopes=app_config.SCOPES)

basedir = os.path.abspath(os.path.dirname(__file__))
os.path.join(basedir, 'templates')
templates = Jinja2Templates(directory=os.path.join(basedir, 'templates'))


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme),
                           token_service: TokenService = Depends(get_token_service)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    try:
        token_data = token_service.decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
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


@router.get('/tokenInfo')
async def token_info(user: User = Security(get_current_user, scopes=['me'])):
    return asdict(user)


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 token_service: TokenService = Depends(get_token_service)):
    credentials: Credentials = Credentials(form_data.username, form_data.password)
    logger.info(f'Creating token for {form_data.username}')
    access_token_expires = timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    try:
        access_token = token_service.create_access_token(form_data.username, credentials=credentials,
                                                         expires_delta=access_token_expires, scopes=form_data.scopes)
    except (UserNotFound, UserServiceConnectionError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ScopeNotAllowedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expire_in": app_config.ACCESS_TOKEN_EXPIRE_MINUTES
    }


@router.get('/auth', response_class=HTMLResponse)
async def auth(request: Request, client_id: str, redirect_uri: str, scope: str, state: str, response_type: str):
    return templates.TemplateResponse("auth.html", {"request": request, "client_id": client_id,
                                                    "redirect_uri": redirect_uri, "scopes": scope})


@router.post('/signin')
async def signin(username: str = Form(...), password: str = Form(...), client_id: str = Form(...),
                 redirect_uri: str = Form(...), scopes: str = Form(...),
                 token_service: TokenService = Depends(get_token_service)):
    if not client_id_service.client_id_present_in_db(client_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Client id unknown",
            headers={"WWW-Authenticate": "Bearer"},
        )
    credentials: Credentials = Credentials(username, password)
    logger.info(f'Creating token for {username}')
    access_token_expires = timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    try:
        access_token = token_service.create_access_token(username, credentials=credentials,
                                                         expires_delta=access_token_expires, scopes=scopes.split(' '))
    except (UserNotFound, UserServiceConnectionError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ScopeNotAllowedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    # return {"access_token": access_token, "token_type": "bearer"}
    return RedirectResponse(url=process_redirect_url(redirect_uri, {
        'access_token': access_token,
        'token_type': 'Bearer',
        'expires_in': app_config.ACCESS_TOKEN_EXPIRE_MINUTES
    }), status_code=status.HTTP_303_SEE_OTHER)


def process_redirect_url(redirect_url, new_entries):
    # Prepare the redirect URL
    url_parts = list(urlparse.urlparse(redirect_url))
    queries = dict(urlparse.parse_qsl(url_parts[4]))
    queries.update(new_entries)
    url_parts[4] = urlencode(queries)
    url = urlparse.urlunparse(url_parts)
    return url
