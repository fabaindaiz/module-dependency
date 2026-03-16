from dependency.core.injection.injection import ContainerInjection as ContainerInjection, ProviderInjection as ProviderInjection

class Registry:
    containers: set[ContainerInjection]
    providers: set[ProviderInjection]
    @classmethod
    def register_container(cls, container: ContainerInjection) -> None: ...
    @classmethod
    def register_provider(cls, provider: ProviderInjection) -> None: ...
    @classmethod
    def validation(cls) -> None: ...
