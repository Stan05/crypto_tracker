# crypto_tracker/repositories_new/base_repository.py

from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
