from typing import Any, Generic, TypeVar
from dependency_injector import providers

I = TypeVar('I')

class Implementation(Generic[I]):
    def check_generic(self) -> str:
        return str(self.__class__.__name__)

def implementation(
        provider: type[providers.Provider] = providers.Singleton
    ):
    def wrap(cls: type) -> type:
        return cls
    return wrap
        

@implementation(
    provider=providers.Singleton
)
class Formatter:
    def __init__(self, format: str, params: dict[str, type] = {}) -> None:
        self.__format: str = format
        self.__params: dict[str, type] = params

    def __validate_params(self, params: dict[str, Any]) -> bool:
        for key, value in params.items():
            if key not in self.__format:
                print(f"Invalid format key: {key}")
                return False
            if key not in self.__params:
                print(f"Invalid parameter: {key}")
                return False
            if not isinstance(value, self.__params[key]):
                print(f"Invalid type for parameter {key}: expected {self.__params[key].__name__}, got {type(value).__name__}")
                return False
        return True

    def format(self, **kwargs: Any) -> str:
        if not self.__validate_params(kwargs):
            raise ValueError("Invalid parameters")

        return self.__format.format(**kwargs)

if __name__== "__main__":
    formatter = Implementation[Formatter]()
    print(formatter.check_generic())
