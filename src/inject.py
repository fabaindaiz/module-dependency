from src.container import Container
from src.service1.mixin import Service1Mixin
from src.service2.mixin import Service2Mixin

container = Container()
container.init_resources()
container.check_dependencies()

Service1Mixin()._wire(container)
Service2Mixin()._wire(container)