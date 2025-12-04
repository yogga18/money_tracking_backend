# import redis.asyncio as redis
# from money_tracker.core.config import get_settings

# settings = get_settings()

# async def get_redis_client() -> redis.Redis:
#     """
#     Returns an async Redis client.
#     """
#     return redis.from_url(
#         settings.REDIS_URL,
#         encoding="utf-8",
#         decode_responses=True
#     )
