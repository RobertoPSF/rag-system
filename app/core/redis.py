import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
QUEUE_NAME = "ingestion_queue"


def enqueue_document(document_id: int):
    redis_client.lpush(QUEUE_NAME, document_id)


def dequeue_document():
    return redis_client.brpop(QUEUE_NAME, timeout=5)