from fastapi import APIRouter

router = APIRouter()


@router.get('/me')
def me():
    return 'ok'
