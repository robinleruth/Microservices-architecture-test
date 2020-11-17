from typing import List

from app.infrastructure.db import DbClientId
from app.infrastructure.db.db_session import transaction_context


def client_id_present_in_db(client_id: str) -> bool:
    with transaction_context() as session:
        ids = session.query(DbClientId).all()
        ids = set(map(lambda x: x.client_id, ids))
    if client_id in ids:
        return True
    else:
        return False


def add_one(client_id: str):
    with transaction_context() as session:
        entry = DbClientId(client_id=client_id)
        session.add(entry)


def get_all() -> List[str]:
    with transaction_context() as session:
        ids = session.query(DbClientId).all()
        ids = list(map(lambda x: x.client_id, ids))
    return ids
