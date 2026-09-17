"""Reusable building blocks for applications built on the framework.

Nothing here is decorated. These are `Component` subclasses that declare a contract,
and mixins that supply an implementation body — the application applies `@component`
and `@instance` itself.

That split is deliberate and measured; see D-030 in docs/decisions.md. Declaration is a
global import-time side effect, and `Injectable.set_implementation` is last-wins, so a
decorated component shipped from a library would make the active implementation depend on
import order rather than on intent.
"""

from dependency.library.components.observer import (
    EventPublisherMixin,
    ObserverComponent,
)

__all__ = [
    "EventPublisherMixin",
    "ObserverComponent",
]
