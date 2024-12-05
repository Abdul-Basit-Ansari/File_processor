from pydantic import BaseModel

class FileResponseSchema(BaseModel):
    """Schema for formatting the response after processing a file."""
    file_name: str
    user_id: int
    content: str