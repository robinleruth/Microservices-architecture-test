from requests import Session
from tcommon import TokenAuth

if __name__ == '__main__':
    s = Session()
    s.auth = TokenAuth(username='Robin', password='test', scopes=['me'])

    r = s.get('http://localhost:8082/api/v1/token_controller/tokenInfo')

    print(r.json())
