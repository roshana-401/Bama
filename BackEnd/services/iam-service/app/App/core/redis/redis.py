import redis
from App.core.config import setting

try:
    redis_client = redis.StrictRedis(
        host=setting.redis_url,
        port=6379,
        charset="utf-8",
        decode_responses=True
    )

except Exception as e:
    redis_client = None


def get_redis_client():
    return redis_client
