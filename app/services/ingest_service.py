from sqlalchemy.orm import Session
from app.db import models


def create_document(db: Session, filename: str, content: bytes):
    document = models.Document(
        filename=filename,
        content=content.decode("utf-8"),
        status="pending",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document