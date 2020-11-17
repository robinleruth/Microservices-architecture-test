from fastapi import Security, HTTPException
from fastapi.openapi.models import OAuthFlows, OAuthFlowImplicit
from fastapi.security import OAuth2
from starlette import status

from tcommon.authenticate_token import get_user_info_by_token, UnauthorizedException
from tcommon.config import app_config

url = app_config.TOKEN_SERVICE_URL + app_config.TOKEN_CREATION
oauth2_scheme: OAuth2 = OAuth2(
    flows=OAuthFlows(implicit=OAuthFlowImplicit(authorizationUrl=url + f'&client_id={app_config.CLIENT_ID}',
                                                scopes={'test': 'test'})))


def get_user_implicit(token: str = Security(oauth2_scheme)):
    try:
        user = get_user_info_by_token(token)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Could not authenticate')
    return user
