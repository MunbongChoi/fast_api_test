import redis
from src.config import settings

# Redis 클라이언트 연결
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

def get_cached_value(key: str):
    return redis_client.get(key)

def set_cached_value(key: str, value: str, expire_seconds=300):
    redis_client.set(key, value, ex=expire_seconds)
