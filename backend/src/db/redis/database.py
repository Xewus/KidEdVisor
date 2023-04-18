from redis import Redis
from redis.exceptions import ConnectionError
from src.config import settings


class RedisDB:
    """Connection to Redis database."""

    __host = settings.redis_host
    __port = settings.redis_port

    @classmethod
    def get_db(cls, db: int | None = 0) -> Redis:
        """Get connection to Redis database.

        #### Args:
        - db (int | None): Default `0`.
            Database number to connect to.

        #### Returns:
        - Redis:
            Connection to Redis database.
        """
        return Redis(
            host=cls.__host,
            port=cls.__port,
            db=db,
        )


default_db = RedisDB.get_db()
auth_db = RedisDB.get_db(settings.redis_auth_db)
cache_db = RedisDB.get_db(settings.redis_cache_db)


def check_redis() -> None:
    """Check connection to Redis.

    #### Raises:
    - ConnectionError:
        No connection to Redis.
    """
    if not default_db.ping():
        raise ConnectionError("\n\n\033[101mNo connection to Redis!\033[0m\n")
    if not auth_db.ping():
        raise ConnectionError("\n\n\033[101mNo connection to Redis!\033[0m\n")
    if not cache_db.ping():
        raise ConnectionError("\n\n\033[101mNo connection to Redis!\033[0m\n")
    return None
