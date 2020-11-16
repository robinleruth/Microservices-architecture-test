import uvicorn

from app.infrastructure.config import app_config
from app.interface import api

if __name__ == '__main__':
    uvicorn.run(api, port=app_config.PORT, host='0.0.0.0')
