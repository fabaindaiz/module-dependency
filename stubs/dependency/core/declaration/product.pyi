from dependency.core.declaration.component import Component
from typing import Callable, TypeVar

PRODUCT = TypeVar('PRODUCT', bound='Product')

class Product:
    """Product Base Class
    """

def product(imports: list[type[Component]] = []) -> Callable[[type[PRODUCT]], type[PRODUCT]]:
    """Decorator for Product class

    Args:
        imports (Sequence[type[Component]], optional): List of components to be imported by the product. Defaults to [].

    Raises:
        TypeError: If the wrapped class is not a subclass of Dependent.

    Returns:
        Callable[[type[Dependent]], type[Dependent]]: Decorator function that wraps the dependent class.
    """
