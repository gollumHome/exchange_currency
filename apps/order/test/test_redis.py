# coding: utf-8


from apps.redis_client import RedisClient

redis_api = RedisClient()


print(redis_api.subscribe_order('xx'))

#print(redis_api.set_expired('xxx',5))
print("*" * 20)
#print(redis_api.redis_client.pubsub_channels())