from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2
from tcommon.oauth_implem import OauthImplem

from app.domain.model.event import EventIn, Event
from app.domain.services.event_service.bean import get_event_service
from app.domain.services.event_service.event_service import EventService
from app.domain.services.event_store.bean import get_event_store
from app.domain.services.event_store.event_store import EventStore
from app.infrastructure.config import app_config

router = APIRouter()

oauth_implem = OauthImplem(scopes=app_config.SCOPES, client_id=app_config.CLIENT_ID)


@router.post('/sendEvent', response_model=Event)
async def send_event(event: EventIn, event_service: EventService = Depends(get_event_service),
                     oauth: OAuth2 = Security(oauth_implem.get_user_implicit(), scopes=['event'])):
    return await event_service.process_event(event)


@router.get('/getAuditTrail')
async def get_audit_trail(aggregate_id: str, event_store: EventStore = Depends(get_event_store)):
    return await event_store.get_aggregate(aggregate_id)
