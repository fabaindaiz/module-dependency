"""Pytest fixtures for applications built with this framework.

Registered through the ``pytest11`` entry point, so this module loads in **every**
environment where ``module_dependency[testing]`` is installed. Nothing here is
``autouse``: a plugin that changes behaviour merely by being installed is a plugin that
breaks somebody's suite on upgrade.

What it cannot do yet is the point of it existing now. ``dependency_container`` hands out
a fresh ``Container``, which is the isolation boundary this repository documents (D-023).
Declaration state is **not** covered by that boundary: ``injection``, ``injectable``, the
resolved flag, the adopted parent and the provider instance are class attributes written
at import time with no teardown path. ``declaration_state`` measures exactly that, and
``tests/testing/test_plugin.py`` pins the gap with a strict xfail that will begin failing
the day the gap closes.

**Every framework import in this module is deferred into the function that needs it, and
that is not style.** Pytest loads entry-point plugins *before* ``pytest-cov`` starts
measuring, so anything this module imports at module level is executed unmeasured and every
statement in it is then reported as never run. Measured when this file imported
``dependency.core`` at the top: coverage of ``core/`` read **59%** instead of **95%**, and
``core/__init__.py`` read 0%. Moving an import back to the top of this file silently
destroys the coverage number for the whole package.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any
import pytest

if TYPE_CHECKING:  # pragma: no cover
    from dependency.core.injection.mixin import ProviderMixin
    from dependency.core.resolution.container import Container

@pytest.fixture
def dependency_container() -> Container:
    """A fresh application `Container`, built empty.

    This is the isolation boundary the suite relies on (D-023): providers attached to one
    container are invisible to another. It does **not** isolate declaration state.
    """
    from dependency.core.resolution.container import Container

    return Container.from_dict({})

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
    from dependency.core.exceptions import DeclarationError

    snapshot: dict[str, Any] = {}
    for provided_cls in declared:
        node = provided_cls.injection
        key = provided_cls.__qualname__
        snapshot[f"{key}.is_resolved"] = node.is_resolved
        snapshot[f"{key}.parent"] = node.parent.name if node.parent is not None else None
        snapshot[f"{key}.implementation"] = provided_cls.injectable.implementation
        try:
            snapshot[f"{key}.provider"] = id(node.provider)
        except DeclarationError:
            snapshot[f"{key}.provider"] = None
    return snapshot
