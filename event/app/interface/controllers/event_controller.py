from fastapi import APIRouter

router = APIRouter()


@router.post('/sendEvent')
async def send_event():
    pass
