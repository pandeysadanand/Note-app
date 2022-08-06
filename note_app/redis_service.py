import redis


class RedisService:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        """
        for getting the cache
        :param key: getting the key as user_id
        :return: values
        """
        return self.cache.get(key)

    def set(self, key, value):
        """
        for inserting in the cache
        :param key: key as user_id
        :param value: value will be note data
        :return: key and value
        """
        return self.cache.set(key, value)