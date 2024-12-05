from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from ..db.database import SessionLocal
from ..schemas.file_schema import FileResponseSchema
from ..services.file_service import FileService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()

STATIC_TOKEN = "TopSecret_Token"
ALLOWED_EXTENSIONS = {".xlsx", ".txt", ".csv", ".json"}

# Dependency to get a database session
def get_db():
    """Provide a database session for each request."""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# Dependency to verify Bearer token authentication.
security = HTTPBearer()

async def verify_token(auth: HTTPAuthorizationCredentials = Depends(security)):
    if auth.credentials != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")

@router.post("/process-file/", response_model=FileResponseSchema)
async def process_file(
    file: UploadFile = File(...),
    user_id: int = 1,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(verify_token)
):

    service = FileService(db)
    if not service.allowed_file(filename= file.filename, ALLOWED_EXTENSIONS= ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx, .txt, .csv, and .json are allowed.")
    
    file_content = await file.read()
    file_type = service.get_file_extention(file.filename)

    # Process the file using the service
    return service.process_file(file_content, user_id, file_type)
