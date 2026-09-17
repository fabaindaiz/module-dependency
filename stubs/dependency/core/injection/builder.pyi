from dependency.core.exceptions import DeclarationError as DeclarationError
from dependency.core.injection.graph import ApplicationGraph as ApplicationGraph
from dependency.core.injection.injectable import Injectable as Injectable
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection
from dependency.core.injection.mixin import ContainerMixin as ContainerMixin, ProviderMixin as ProviderMixin
from dependency.core.injection.spec import ComponentSpec as ComponentSpec, ImplementationSpec as ImplementationSpec, own_component_spec as own_component_spec, own_implementation_spec as own_implementation_spec, own_module_spec as own_module_spec
from typing import Iterable

class GraphBuilder:
    """Builds one `ApplicationGraph` from whatever has been declared and imported."""
    def __init__(self, roots: Iterable[type]) -> None:
        """
        Args:
            roots: The `Plugin` classes this application is built from.
        """
    def build(self) -> ApplicationGraph:
        """Structure and bind in one call, for callers with nothing to import between."""
    def structure(self) -> ApplicationGraph:
        """Build the container tree. No component node exists yet."""
    def bind(self, graph: ApplicationGraph) -> None:
        """Create a node per reachable component and bind exactly one implementation to each.

        Reachable means: declared under one of this build's roots, or imported — directly or
        transitively — by something that is. A component declared elsewhere in the process is
        not this application's business, and building a node for it would make every
        declaration anywhere a participant in every build.
        """
