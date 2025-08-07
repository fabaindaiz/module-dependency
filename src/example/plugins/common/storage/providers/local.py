from dependency.core.declaration.instance import instance, providers
from example.plugins.common.storage import StorageService, StorageServiceComponent

@instance(
    component=StorageServiceComponent,
    provider=providers.Singleton,
    bootstrap=True,
)
class LocalStorageService(StorageService):
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}
        print("LocalStorageService initialized")

    def get(self, key: str) -> str:
        return self.storage.get(key, "")

    def set(self, key: str, value: str) -> None:
        self.storage[key] = value