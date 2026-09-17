import pytest
from dependency.core.injection.mixin import ProviderMixin as ProviderMixin
from dependency.core.resolution.container import Container as Container
from typing import Any

@pytest.fixture
def dependency_container() -> Container:
    """A fresh application `Container`, built empty.

    This is the isolation boundary the suite relies on (D-023): providers attached to one
    container are invisible to another. It does **not** isolate declaration state.
    """
def declaration_state(*declared: type[ProviderMixin]) -> dict[str, Any]:
    """Snapshot the mutable declaration state carried by the given component classes.

    Every value read here lives on the class object and is never reset. Take a snapshot
    before an operation and another after it to see precisely what the operation left
    behind in the process.

    Args:
        declared: Component classes to snapshot.

    Returns:
        dict[str, Any]: One entry per observed attribute, keyed by `<class>.<attribute>`.
    """
