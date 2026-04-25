import time
import traceback

from app.core.redis import dequeue_document
from app.db.session import SessionLocal
from app.db import models
from app.services.processing_service import process_document


def run_worker():
    print("Worker started...")
    while True:
        job = dequeue_document()
        if job:
            _, document_id = job
            db = SessionLocal()
            try:
                document = db.get(models.Document, document_id)
                if not document or document.status == "completed":
                    return

                document.status = "processing"
                db.commit()

                process_document(db, document)

                document.status = "completed"
                db.commit()

            except Exception as e:
                traceback.print_exc()
                document.status = "failed"
                db.commit()
            finally:
                db.close()
        else:
            time.sleep(1)


if __name__ == "__main__":
    run_worker()