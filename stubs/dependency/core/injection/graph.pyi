from dependency.core.exceptions import DeclarationError as DeclarationError
from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection

class ApplicationGraph:
    """The materialised injection tree of one application build.

    Attributes:
        roots: The `ContainerInjection` nodes of the plugins this graph was built from.
    """
    roots: tuple[ContainerInjection, ...]
    def __init__(self, roots: tuple[ContainerInjection, ...], containers: dict[type, ContainerInjection], nodes: dict[type, ProviderInjection]) -> None: ...
    @property
    def components(self) -> tuple[type, ...]:
        """Every component class that has a node in this graph."""
    @property
    def modules(self) -> tuple[type, ...]:
        """Every module class that has a container in this graph."""
    def add_node(self, component_cls: type, node: ProviderInjection) -> None:
        """Record the provider node of a component. Called once per build, by the builder."""
    def node(self, component_cls: type) -> ProviderInjection:
        """The provider node for a component class.

        Raises:
            DeclarationError: If the class has no node in this graph.
        """
    def container_for(self, module_cls: type) -> ContainerInjection:
        """The container node for a module class.

        Raises:
            DeclarationError: If the class has no container in this graph.
        """
    def implementation_of(self, component_cls: type) -> type | None:
        """The concrete class bound to a component in this build, if any."""
