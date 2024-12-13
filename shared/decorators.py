import json
from functools import wraps

from setup.adapters.cache import RedisCache


def introspect_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = f"{func.__name__}{str(args)}"
        response = RedisCache.get(key)
        if not response:
            response = func(*args, **kwargs)
            RedisCache.set(key, json.dumps(response))
            return response
        else:
            return json.loads(response)

    return wrapper
