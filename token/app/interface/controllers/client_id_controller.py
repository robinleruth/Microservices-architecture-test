import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from app.domain.services.client_id import client_id_service
from app.infrastructure.config import app_config
from app.interface.schemas.client_id import ClientId

router = APIRouter()

security = HTTPBasic()


def get_admin_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_name = secrets.compare_digest(credentials.username, app_config.ADMIN_USER)
    correct_pwd = secrets.compare_digest(credentials.password, app_config.ADMIN_PWD)
    if not (correct_name and correct_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect name or password',
            headers={'WWW-Authenticate': 'Basic'}
        )
    return credentials.username


@router.get('/all')
async def get_all(admin: str = Depends(get_admin_user)):
    return client_id_service.get_all()


@router.post('/addOne', status_code=status.HTTP_201_CREATED)
async def add_one(client_id: ClientId, admin: str = Depends(get_admin_user)):
    client_id_service.add_one(client_id.client_id)
    return "Ok"
