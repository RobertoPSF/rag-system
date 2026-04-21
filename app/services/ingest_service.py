from sqlalchemy.orm import Session
from app.db import models
from app.core.redis import enqueue_document
import hashlib


def create_document_and_enqueue(db: Session, filename: str, content: bytes):
    content_str = content.decode("utf-8")
    content_hash = hashlib.sha256(content).hexdigest()

    existing = db.query(models.Document).filter_by(content_hash=content_hash).first()
    if existing:
        return existing

    document = models.Document(
        filename=filename,
        content=content_str,
        content_hash=content_hash,
        status="queued",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    enqueue_document(document.id)

    return document