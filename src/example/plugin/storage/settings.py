from pydantic import BaseModel


class StorageSettings(BaseModel):
    path: str = "build/readings.jsonl"
    keep_last: int = 100


class StorageConfig(BaseModel):
    storage: StorageSettings = StorageSettings()
