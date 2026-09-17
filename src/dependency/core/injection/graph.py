"""One built application: its containers, its provider nodes, and their bindings.

Everything mutable about a running application lives here — the tree, the bindings, the
provider instances, the resolved flags — and is discarded with the graph. Two graphs built
from the same declarations share nothing.

The declarations themselves are immutable specs on the class objects, so a graph is derived
data: build it, use it, throw it away, build another.
"""

from typing import Optional
from dependency.core.injection.injection import ContainerInjection, ProviderInjection
from dependency.core.exceptions import DeclarationError


class ApplicationGraph:
    """The materialised injection tree of one application build.

    Attributes:
        roots: The `ContainerInjection` nodes of the plugins this graph was built from.
    """

    def __init__(
        self,
        roots: tuple[ContainerInjection, ...],
        containers: dict[type, ContainerInjection],
        nodes: dict[type, ProviderInjection],
    ) -> None:
        self.roots: tuple[ContainerInjection, ...] = roots
        self._containers: dict[type, ContainerInjection] = containers
        self._nodes: dict[type, ProviderInjection] = nodes

    @property
    def components(self) -> tuple[type, ...]:
        """Every component class that has a node in this graph."""
        return tuple(self._nodes)

    @property
    def modules(self) -> tuple[type, ...]:
        """Every module class that has a container in this graph."""
        return tuple(self._containers)

    def add_node(self, component_cls: type, node: ProviderInjection) -> None:
        """Record the provider node of a component. Called once per build, by the builder."""
        self._nodes[component_cls] = node

    def node(self, component_cls: type) -> ProviderInjection:
        """The provider node for a component class.

        Raises:
            DeclarationError: If the class has no node in this graph.
        """
        node = self._nodes.get(component_cls)
        if node is None:
            raise DeclarationError(
                f"Component {component_cls.__name__} has no node in this application graph. "
                f"It was never declared with @component, or its module was not reached."
            )
        return node

    def container_for(self, module_cls: type) -> ContainerInjection:
        """The container node for a module class.

        Raises:
            DeclarationError: If the class has no container in this graph.
        """
        container = self._containers.get(module_cls)
        if container is None:
            raise DeclarationError(
                f"Module {module_cls.__name__} has no container in this application graph."
            )
        return container

    def implementation_of(self, component_cls: type) -> Optional[type]:
        """The concrete class bound to a component in this build, if any."""
        return self.node(component_cls).injectable.implementation
