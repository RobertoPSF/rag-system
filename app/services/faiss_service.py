import faiss
import numpy as np

index = None

def get_or_create_index(dimension: int):
    global index
    if index is None:
        index = faiss.IndexFlatL2(dimension)
    return index


def add_to_index(doc_id, chunk_id, embedding):
    vector = np.array([embedding]).astype("float32")

    idx = get_or_create_index(len(embedding))
    idx.add(vector)