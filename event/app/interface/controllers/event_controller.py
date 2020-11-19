from fastapi import APIRouter, Depends

from app.domain.model.event import EventIn, Event
from app.domain.services.event_store.bean import get_event_store
from app.domain.services.event_store.event_store import EventStore

router = APIRouter()


@router.post('/sendEvent', response_model=Event)
async def send_event(aggregate: EventIn, event_store: EventStore = Depends(get_event_store)):
    if aggregate.aggregate_id is None:
        aggregate.aggregate_id = event_store._generate_uuid()
    return aggregate


@router.get('/getAuditTrail')
async def get_audit_trail(aggregate_id: str):
    pass
