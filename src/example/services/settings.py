from pydantic import BaseModel

class Keys(BaseModel):
    key1: str
    key2: str

class Config(BaseModel):
    factory: Keys
    singleton: Keys