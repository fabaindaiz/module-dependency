from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from abc import ABC, abstractmethod

class Service(ABC):
    @abstractmethod
    def work(self):
        pass

class Service1(Service):
    def work(self):
        print("Service1 work")


class ServiceProvider(containers.DeclarativeContainer):
    service = providers.Singleton(Service)

@containers.override(ServiceProvider)
class Service1Provider(containers.DeclarativeContainer):
    service = providers.Singleton(Service1)

class Container(containers.DeclarativeContainer):
    service_container = providers.Container(ServiceProvider)


class ServiceMixin:
    _service: Service = Provide[Container.service_container.service]

    @property
    def service(self) -> Service:
        return self._service
    
    @staticmethod
    def _wire(container):
        return container.wire(modules=[ServiceMixin])

container = Container()
container.init_resources()
ServiceMixin._wire(container)


class Worker(ServiceMixin):
    def do_work(self):
        self.service.work()

Worker().do_work()