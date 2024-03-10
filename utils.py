import requests
API = 'https://www.fruityvice.com/api/fruit/all'


import json
from functools import wraps


def cache_function_result(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper

@cache_function_result
def get_fruits():
    response = requests.get(API).json()
    return response
