import uvicorn
import requests

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return 'ok from token'


@app.get('/test_from_other_api')
def test_from_other_api():
    r = requests.get('http://users:8080/')
    return r.json()


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
