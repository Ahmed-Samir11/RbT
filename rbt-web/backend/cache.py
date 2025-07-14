REDIS_AVAILABLE = False
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    pass

if REDIS_AVAILABLE:
    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.redis import RedisBackend
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    def init_cache(app=None):
        FastAPICache.init(RedisBackend(r), prefix="rbt-cache")
else:
    _MEM_CACHE = {}
    def init_cache(app=None):
        pass

class SimpleCache:
    def get(self, key):
        if REDIS_AVAILABLE:
            return r.get(key)
        else:
            return _MEM_CACHE.get(key)
    def set(self, key, value, expire=300):
        if REDIS_AVAILABLE:
            r.set(key, value, ex=expire)
        else:
            _MEM_CACHE[key] = value

cache = SimpleCache()
