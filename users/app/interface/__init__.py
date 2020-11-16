from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(title='Users API',
              description='',
              version='0.1')

from .controllers import user_controller

api.include_router(user_controller.router,
                   prefix='/api/v1/user_controller',
                   tags=['user_controller'])

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
