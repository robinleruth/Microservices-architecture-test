from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..domain.services.token.bean import get_token_service

api = FastAPI(title='Token API',
              description='',
              version='0.1')

from .controllers import token_controller

api.include_router(token_controller.router,
                   prefix='/api/v1/token_controller',
                   tags=['token_controller'])

from .controllers import client_id_controller

api.include_router(client_id_controller.router,
                   prefix='/api/v1/client_id_controller',
                   tags=['client_id_controller'])

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.on_event('startup')
async def startup():
    get_token_service()
