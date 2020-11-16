from contextlib import contextmanager

from app.infrastructure.db import Session


@contextmanager
def transaction_context():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        Session.remove()

