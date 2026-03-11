import redis
import json
from flask import current_app

redis_client = None

def init_redis(app):
    global redis_client
    redis_client = redis.from_url(app.config['REDIS_URL'])
    return redis_client

def get_redis_client():
    global redis_client
    if redis_client is None:
        from flask import current_app
        redis_client = redis.from_url(current_app.config['REDIS_URL'])
    return redis_client

def cache_set(key, value, expiry=3600):
    client = get_redis_client()
    client.setex(key, expiry, json.dumps(value))

def cache_get(key):
    client = get_redis_client()
    value = client.get(key)
    if value:
        return json.loads(value)
    return None

def cache_delete(key):
    client = get_redis_client()
    client.delete(key)

def cache_clear_pattern(pattern):
    client = get_redis_client()
    keys = client.keys(pattern)
    if keys:
        client.delete(*keys)

def cache_invalidate(entity_type, entity_id=None):
    pattern = f"{entity_type}:*" if entity_id is None else f"{entity_type}:{entity_id}:*"
    cache_clear_pattern(pattern)
