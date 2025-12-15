from typing import Callable, TypeVar
from dependency.core.declaration.component import Component
from dependency.core.injection.base import ProviderDependency

PRODUCT = TypeVar('PRODUCT', bound='Product')

class Product:
    """Product Base Class
    """
    dependency_imports: ProviderDependency

def product(
    imports: list[Component] = []
) -> Callable[[type[PRODUCT]], type[PRODUCT]]:
    """Decorator for Product class

    Args:
        imports (Sequence[type[Component]], optional): List of components to be imported by the product. Defaults to [].

    Raises:
        TypeError: If the wrapped class is not a subclass of Dependent.

    Returns:
        Callable[[type[Dependent]], type[Dependent]]: Decorator function that wraps the dependent class.
    """
    def wrap(cls: type[PRODUCT]) -> type[PRODUCT]:
        if not issubclass(cls, Product):
            raise TypeError(f"Class {cls} is not a subclass of Product")

        cls.dependency_imports = ProviderDependency(
            name=cls.__name__,
            provided_cls=cls,
            imports=[component.injection for component in imports])
        return cls
    return wrap