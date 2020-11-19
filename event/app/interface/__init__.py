from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(title='Token API',
              description='',
              version='0.1')

from .controllers import event_controller

api.include_router(event_controller.router,
                   prefix='/api/v1/event_controller',
                   tags=['event_controller'])

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
