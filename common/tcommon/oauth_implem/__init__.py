# TODO: Authorization code and client credentials implem

from fastapi import Security, HTTPException
from fastapi.openapi.models import OAuthFlows, OAuthFlowImplicit
from fastapi.security import OAuth2
from starlette import status

from tcommon.authenticate_token import get_user_info_by_token, UnauthorizedException
from tcommon.config import app_config

url = app_config.TOKEN_SERVICE_URL + app_config.SIGN_IN_PAGE
oauth2_scheme: OAuth2 = OAuth2(flows=OAuthFlows(
    implicit=OAuthFlowImplicit(authorizationUrl=url + f'?client_id={app_config.CLIENT_ID}',
                               # TODO: get Scopes from app_config of real service
                               scopes=app_config.SCOPES)))


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
