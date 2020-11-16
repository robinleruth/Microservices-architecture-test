from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(title='Token API',
              description='',
              version='0.1')

from .controllers import token_controller

api.include_router(token_controller.router,
                   prefix='/api/v1/token_controller',
                   tags=['token_controller'])

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
