from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.db import models
import json

from app.services.embedding_service import generate_embedding
from app.services.faiss_service import add_to_index


def process_document(db, document):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(document.content)

    chunk_entities = []
    total_tokens = 0

    for i, chunk_text in enumerate(chunks):
        embedding = generate_embedding(chunk_text)

        chunk = models.Chunk(
            document_id=document.id,
            content=chunk_text,
            chunk_index=i,
            embedding=json.dumps(embedding)
        )

        chunk_entities.append(chunk)
        total_tokens += len(chunk_text)

        add_to_index(document.id, i, embedding)

    db.add_all(chunk_entities)

    stats = models.Stats(
        document_id=document.id,
        total_chunks=len(chunks),
        total_tokens=total_tokens
    )

    db.add(stats)
    db.commit()

    add_to_index(document.id, i, embedding)

    stats = models.Stats(
        document_id=document.id,
        total_chunks=len(chunks),
        total_tokens=sum(len(c) for c in chunks)
    )

    db.add(stats)
    db.commit()