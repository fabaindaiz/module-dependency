from dependency.core.declaration import instance, providers
from example.plugins.base.storage.cache import CacheService, CacheServiceComponent
from example.plugins.base.settings import BasePluginConfig

@instance(
    component=CacheServiceComponent,
    provider=providers.Singleton,
)
class RedisCacheService(CacheService):
    def __init__(self, config: BasePluginConfig) -> None:
        self._config = config
        # Initialize Redis connection here using self._config

    def get(self, key: str) -> str:
        # Implement logic to get value from Redis cache
        return "value_from_redis"

    def set(self, key: str, value: str) -> None:
        # Implement logic to set value in Redis cache
        pass