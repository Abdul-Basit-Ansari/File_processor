from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class FileRecord(Base):
    """Model will representing file records in the database."""
    __tablename__ = "file_records"
    
    id = Column(Integer, primary_key=True, index=True)
    file_type = Column(String, index=True)
    user_id = Column(Integer, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
