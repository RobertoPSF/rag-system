from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.ingest_service import create_document_and_enqueue


router = APIRouter()

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    document = create_document_and_enqueue(db, file.filename, content)
    return {"document_id": document.id}