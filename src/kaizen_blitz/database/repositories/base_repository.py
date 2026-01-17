"""Base repository for common database operations."""

from typing import TypeVar, Generic, List, Optional, Type, Dict, Any

from sqlalchemy.orm import Session

from ...config.database import SessionLocal
from ...models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    """Generic base repository for database operations."""
    
    def __init__(self, model: Type[T]):
        """Initialize repository with a model class.
        
        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model
        self.session: Optional[Session] = None
    
    def _get_session(self) -> Session:
        """Get or create a database session.
        
        Returns:
            Database session.
        """
        if self.session is None:
            self.session = SessionLocal()
        return self.session
    
    def get_all(self) -> List[T]:
        """Get all records.
        
        Returns:
            List of all model instances.
        """
        session = self._get_session()
        return session.query(self.model).all()
    
    def get_by_id(self, record_id: str) -> Optional[T]:
        """Get a record by ID.
        
        Args:
            record_id: The record ID (UUID string).
        
        Returns:
            Model instance or None if not found.
        """
        session = self._get_session()
        return session.query(self.model).filter(self.model.id == record_id).first()
    
    def create(self, obj: T) -> T:
        """Create a new record.
        
        Args:
            obj: Model instance to create.
        
        Returns:
            Created model instance.
        """
        session = self._get_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    
    def update(self, obj: T) -> T:
        """Update an existing record.
        
        Args:
            obj: Model instance to update.
        
        Returns:
            Updated model instance.
        """
        session = self._get_session()
        session.merge(obj)
        session.commit()
        return obj
    
    def delete(self, record_id: str) -> bool:
        """Delete a record by ID.
        
        Args:
            record_id: The record ID (UUID string).
        
        Returns:
            True if deleted, False if not found.
        """
        session = self._get_session()
        obj = self.get_by_id(record_id)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False
    
    def search(self, **filters: Any) -> List[T]:
        """Search records by filters.
        
        Args:
            **filters: Filter criteria as keyword arguments.
        
        Returns:
            List of matching model instances.
        """
        session = self._get_session()
        query = session.query(self.model)
        
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        
        return query.all()
    
    def close(self) -> None:
        """Close the database session."""
        if self.session:
            self.session.close()
            self.session = None
