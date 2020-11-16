import uvicorn
from fastapi import FastAPI

from interface import api

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(api, port=8080, host='0.0.0.0')
