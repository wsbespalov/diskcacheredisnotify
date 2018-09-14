import redis

channel = 'cwe:notifications:*'

cache = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0
)