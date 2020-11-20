# TODO: Authorization code and client credentials implem
from typing import List

from fastapi import Security, HTTPException
from fastapi.openapi.models import OAuthFlows, OAuthFlowImplicit
from fastapi.security import OAuth2, SecurityScopes
from starlette import status

from tcommon.authenticate_token import get_user_info_by_token, UnauthorizedException
from tcommon.config import app_config

url = app_config.TOKEN_SERVICE_URL + app_config.SIGN_IN_PAGE


class OauthImplem:
    def __init__(self, scopes: List[str], client_id: str):
        self.scopes = scopes
        self.oauth2_scheme: OAuth2 = OAuth2(flows=OAuthFlows(
            implicit=OAuthFlowImplicit(authorizationUrl=url + f'?client_id={client_id}',
                                       scopes=self.scopes)))

    def get_user_implicit(self):
        def inner(security_scopes: SecurityScopes, token: str = Security(self.oauth2_scheme)):
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
            if not user.has_scopes(security_scopes.scopes):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail=f'User {user.nickname} is not allowed for scope {" ".join(user.scopes_not_allowed)}')
            return user

        return inner
