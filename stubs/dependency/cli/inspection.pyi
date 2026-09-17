from dependency.core.agrupation.plugin import Plugin as Plugin
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.resolution.container import Container as Container
from dependency.core.resolution.resolver import InjectionResolver as InjectionResolver
from dependency.core.resolution.strategy import ResolutionStrategy as ResolutionStrategy
from typing import Any, Iterable

class EntrypointError(Exception):
    """The `module:attribute` spec could not be turned into a list of plugins."""

def load_plugins(spec: str) -> list[type[Plugin]]:
    """Resolve a `package.module:ATTRIBUTE` spec into plugin classes.

    The attribute may be a single `Plugin` subclass or an iterable of them, which is the
    shape an application's `plugins.py` already has.

    Args:
        spec: `package.module:ATTRIBUTE`.

    Raises:
        EntrypointError: If the spec is malformed, unimportable, or does not name plugins.

    Returns:
        list[type[Plugin]]: The plugin classes named by the spec.
    """
def import_modules(names: Iterable[str]) -> None:
    """Import modules for their registration side effect.

    This is how an implementation enters a build (D-008): an `@instance` registers itself
    when its module is imported. Without these, a graph that is fine reports every
    component as unimplemented.

    Raises:
        EntrypointError: If a module cannot be imported.
    """
def expand(plugins: Iterable[type[Plugin]], config: dict[str, Any] | None = None) -> set[ProviderInjection]:
    '''Attach the plugins to a throwaway container, expand the graph and resolve it.

    Two of the four resolution stages run: expansion, which discovers the providers and
    reports anything unsatisfiable with its import chain, and the topological pass, which
    is what actually proves an order exists. **Wiring and bootstrap deliberately do not
    run** — this answers "does this graph hold", not "does this application work", and it
    must be safe to run against somebody else\'s code in CI.

    Raises:
        ResolutionError: If a required import has no implementation, or no order exists.

    Returns:
        set[ProviderInjection]: Every provider that entered resolution.
    '''
def describe(plugins: Iterable[type[Plugin]]) -> list[str]:
    """Render the declared injection tree as indented lines, deepest detail last."""
