# import asyncio
# from typing import List

# import aioredis
# from aioredis import Redis
# from aioredis.pubsub import Channel
# from aioredis.connection import RedisConnection


# class Sample:
#     def __init__(self):
#         self._channels: List[str] = []

#     async def connect(self):
#         use_sentinel = False
#         if use_sentinel:
#             sentinel = await aioredis.create_sentinel(
#                 [
#                     ("192.168.33.11", 26379),
#                     ("192.168.33.12", 26379),
#                     ("192.168.33.13", 26379),
#                 ]
#             )
#             self._redis: Redis = sentinel.master_for("mymaster")
#         else:
#             self._redis: Redis = await aioredis.create_redis_pool(
#                 ("192.168.33.11", 6379)
#             )

#         self._last_pubsub_connection: RedisConnection = None

#     async def health_check_task(self):
#         while True:
#             await asyncio.sleep(3)
#             try:
#                 if not await self.health_check():
#                     await self.reconnect()
#             except Exception as e:
#                 print(f"Health check error: {e}")

#     async def health_check(self) -> bool:
#         """Return True if the internal Pub/Sub connection is OK.
#         """

#         if not self._channels:
#             # Not subscribed yet.
#             return True

#         print("=== Health Check ===")

#         # I couldn't find out a better way to get the internal _pubsub_conn.
#         conn, address = self._redis.connection.get_connection("SUBSCRIBE")

#         if not conn:
#             print("No connection")
#             return False

#         print(f"master: {self._redis.address} / pubsub: {address}")

#         # With Sentinel, "DEBUG SLEEP xx" at master can cause this situation.
#         if self._redis.address != address:
#             print(
#                 "Master address and pub/sub address is not same."
#                 "Failover and yet connected to replica?"
#             )
#             return False

#         pong = await conn.execute("PING")
#         if pong != b"PONG":
#             print("PING failed")
#             return False

#         # "CLIENT KILL ID xx" can cause this situation.
#         if not self._redis.in_pubsub:
#             print("Redis client is working but the pub/sub connection has been lost")
#             return False

#         if self._last_pubsub_connection and conn != self._last_pubsub_connection:
#             print("Connection object is not same with the last one. May be reconnected")
#             return False

#         self._last_pubsub_connection = conn
#         print("Health check OK")

#         return True

#     async def reconnect(self):
#         print("Reconnecting...")
#         old_redis = self._redis

#         # Replace Redis instance with new one
#         await self.connect()

#         print("Unsubscribe all channels")
#         await self.unsubscribe_all(old_redis)

#         print("Re-subscribe all channels")
#         await self.resubscribe_all()
#         print("Reconnected")

#     async def unsubscribe_all(self, old_redis: Redis):
#         if self._channels:
#             await old_redis.unsubscribe(*self._channels)

#     async def resubscribe_all(self):
#         if self._channels:
#             channels = await self._redis.subscribe(*self._channels)
#             for ch in channels:
#                 asyncio.create_task(self.reader(ch))

#     async def pub(self):
#         i = 0
#         while True:
#             i += 1
#             print("--- PUB ---")
#             msg1 = ["channel:1", ["Hello", i]]
#             msg2 = ["channel:2", ["Redis", i]]
#             print(msg1, msg2)
#             await self._redis.publish_json(*msg1)
#             await self._redis.publish_json(*msg2)
#             await asyncio.sleep(1)

#     async def sub(self, channel: str):
#         res = await self._redis.subscribe(channel)
#         ch = res[0]
#         self._channels.append(channel)
#         asyncio.create_task(self.reader(ch))

#     async def reader(self, ch: Channel):
#         while await ch.wait_message():
#             print(f"---- SUB {ch.name} ----")
#             msg = await ch.get_json()
#             print(msg)


# async def main():
#     sample = Sample()
#     await sample.connect()
#     pub = asyncio.create_task(sample.pub())
#     health_check = asyncio.create_task(sample.health_check_task())

#     await sample.sub("channel:1")
#     await sample.sub("channel:2")
#     await pub
#     await health_check


# if __name__ == "__main__":
#     asyncio.run(main())
