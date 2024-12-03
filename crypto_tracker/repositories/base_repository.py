# crypto_tracker/repositories/base_repository.py

from sqlalchemy import and_, exists
from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List, Any

T = TypeVar('T')  # Generic type for SQLAlchemy models

class BaseRepository(Generic[T]):
    def __init__(self, db_session: Session, model: Type[T]):
        self.db_session = db_session
        self.model = model

    def create(self, obj:T) -> T:
        """Create a new record."""
        self.db_session.add(obj)
        self.db_session.commit()
        self.db_session.refresh(obj)
        return obj

    def get_by_id(self, entity_id: int) -> T:
        """Retrieve a record by ID."""
        return self.db_session.query(self.model).filter(self.model.id == entity_id).first()

    def get_all(self) -> List[T]:
        """Retrieve all records."""
        return self.db_session.query(self.model).all()

    def commit(self):
        self.db_session.commit()

    def close(self):
        self.db_session.close()
