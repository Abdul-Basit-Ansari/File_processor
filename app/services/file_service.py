from io import StringIO
from sqlalchemy.orm import Session
from ..schemas.file_schema import FileResponseSchema
from ..repositories.file_repository import FileRepository
from fastapi import HTTPException
from io import BytesIO
import pandas as pd
import csv
import os

class FileService:
    """Service class for handling file processing logic."""

    def __init__(self, db_session: Session):
        self.repository = FileRepository(db_session)

    def process_file(self, file: BytesIO, user_id: int, file_type: str) -> FileResponseSchema:
        """Process the incoming file request and return the content."""
        file_io = BytesIO(file)
        print( "file_io.", file_type)
        saved_record = self.repository.save_file_record(file_type=file_type, user_id=user_id)

        content = self.read_file(file_io, file_type)

        return FileResponseSchema(
            file_name=saved_record.file_type,
            user_id=saved_record.user_id,
            content=content,
        )

    def read_file(self, file: BytesIO, file_type: str) -> str:
        """Read and process the file based on the file type."""
        file.seek(0)

        if file_type == ".csv":
            return self.process_csv(file)

        elif file_type == ".xlsx":
            return self.process_xlsx(file)

        elif file_type == ".txt":
            return self.process_txt(file)

        elif file_type == ".json":
            return self.process_json(file)

        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Supported types are csv, txt, xlsx, pdf.")

    def process_csv(self, file: BytesIO) -> str:
        """Process CSV files."""
        file_content = file.read().decode('utf-8')
        csv_reader = csv.reader(StringIO(file_content))
        data = list(csv_reader)
        return str(data)

    def process_xlsx(self, file: BytesIO) -> str:
        """Process Excel files."""
        df = pd.read_excel(file)
        return df.to_json(orient="records")

    def process_txt(self, file: BytesIO) -> str:
        """Process Text files."""
        file_content = file.read().decode('utf-8')
        return file_content

    def process_json(self, file: BytesIO) -> str:
        """Process JSON files."""
        file_content = file.read().decode('utf-8')
        return file_content
    
    def allowed_file(self, filename: str, ALLOWED_EXTENSIONS: set) -> bool:
        print(filename)
        """Check if the file extension is allowed."""
        extension = os.path.splitext(filename)[1].lower()
        return extension in ALLOWED_EXTENSIONS


    def get_file_extention(self, filename: str) -> bool:
        """Get file extension."""
        extension = os.path.splitext(filename)[1].lower()
        return extension

