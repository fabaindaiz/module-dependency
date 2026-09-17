"""Answer the framework's own question from a shell: does this graph hold?

The invariant is that the whole dependency graph is validated before the first user object
is constructed (D-001). Everything here exists so that answer is available **without
starting the application**: expansion runs, wiring and bootstrap do not.
"""

from typing import Any, Iterable, Optional
import importlib

from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
from dependency.core.resolution.container import Container
from dependency.core.resolution.resolver import InjectionResolver
from dependency.core.resolution.strategy import ResolutionStrategy


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
    if ":" not in spec:
        raise EntrypointError(
            f"{spec!r} is not a module:attribute spec — try 'myapp.plugins:PLUGINS'"
        )
    module_name, _, attribute = spec.partition(":")
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise EntrypointError(f"cannot import {module_name!r}: {exc}") from exc
    try:
        found: Any = getattr(module, attribute)
    except AttributeError as exc:
        raise EntrypointError(f"{module_name!r} has no attribute {attribute!r}") from exc

    if isinstance(found, type):
        candidates = [found]
    else:
        try:
            candidates = list(found)
        except TypeError as exc:
            raise EntrypointError(
                f"{spec} names {found!r}, which is neither a Plugin subclass nor an "
                f"iterable of them"
            ) from exc
    plugins: list[type[Plugin]] = []
    for candidate in candidates:
        if not (isinstance(candidate, type) and issubclass(candidate, Plugin)):
            raise EntrypointError(
                f"{spec} names {candidate!r}, which is not a Plugin subclass"
            )
        plugins.append(candidate)
    if not plugins:
        raise EntrypointError(f"{spec} names no plugins")
    return plugins


def import_modules(names: Iterable[str]) -> None:
    """Import modules for their registration side effect.

    This is how an implementation enters a build (D-008): an `@instance` registers itself
    when its module is imported. Without these, a graph that is fine reports every
    component as unimplemented.

    Raises:
        EntrypointError: If a module cannot be imported.
    """
    for name in names:
        try:
            importlib.import_module(name)
        except ImportError as exc:
            raise EntrypointError(f"cannot import {name!r}: {exc}") from exc


def expand(
    plugins: Iterable[type[Plugin]],
    config: Optional[dict[str, Any]] = None,
) -> set[ProviderInjection]:
    """Attach the plugins to a throwaway container, expand the graph and resolve it.

    Two of the four resolution stages run: expansion, which discovers the providers and
    reports anything unsatisfiable with its import chain, and the topological pass, which
    is what actually proves an order exists. **Wiring and bootstrap deliberately do not
    run** — this answers "does this graph hold", not "does this application work", and it
    must be safe to run against somebody else's code in CI.

    Raises:
        ResolutionError: If a required import has no implementation, or no order exists.

    Returns:
        set[ProviderInjection]: Every provider that entered resolution.
    """
    modules = list(plugins)
    resolver = InjectionResolver(container=Container.from_dict(config or {}))
    resolver.resolve_modules(modules=modules)
    providers = resolver.resolve_injectables(modules=modules)
    ResolutionStrategy().injection(providers=providers)
    return providers


def describe(plugins: Iterable[type[Plugin]]) -> list[str]:
    """Render the declared injection tree as indented lines, deepest detail last."""
    lines: list[str] = []

    def walk(node: ContainerInjection, depth: int) -> None:
        lines.append(f"{'  ' * depth}{node.name}/")
        for child in sorted(node.childs, key=lambda c: c.name):
            if isinstance(child, ContainerInjection):
                walk(child, depth + 1)
            elif isinstance(child, ProviderInjection):
                implementation = child.injectable.implementation
                state = implementation.__name__ if implementation else "— no implementation"
                mark = "ok" if child.is_resolved else ".."
                lines.append(f"{'  ' * (depth + 1)}[{mark}] {child.name} -> {state}")

    for plugin in plugins:
        walk(plugin.injection, 0)
    return lines
