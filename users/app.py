import uvicorn
import requests

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return 'ok from users'


@app.get('/test_from_other_api')
def index():
    return requests.get('http://token:8080/')


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
