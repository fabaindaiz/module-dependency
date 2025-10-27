from dependency.core.declaration.component import Component as Component
from dependency.core.injection.base import ProviderDependency as ProviderDependency
from typing import Callable, TypeVar

PRODUCT = TypeVar('PRODUCT', bound='Product')

class Product:
    """Product Base Class
    """
    dependency_imports: ProviderDependency

def product(imports: list[Component] = []) -> Callable[[type[PRODUCT]], type[PRODUCT]]:
    """Decorator for Product class

    Args:
        imports (Sequence[type[Component]], optional): List of components to be imported by the product. Defaults to [].

    Raises:
        TypeError: If the wrapped class is not a subclass of Dependent.

    Returns:
        Callable[[type[Dependent]], type[Dependent]]: Decorator function that wraps the dependent class.
    """
