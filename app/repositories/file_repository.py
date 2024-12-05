from sqlalchemy.orm import Session
from datetime import datetime

from ..db.models import FileRecord

class FileRepository:
    """Repository class for managing file records in the database."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_file_record(self, file_type: str, user_id: int) -> FileRecord:
        """Save a new file record to the database."""
        new_file_record = FileRecord(
            file_type=file_type,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.db_session.add(new_file_record)
        self.db_session.commit()
        self.db_session.refresh(new_file_record)
        
        return new_file_record

    def close(self):
        """Close the database session."""
        self.db_session.close()