from dependency_injector import containers, providers

# Step 1: Providers injection
from src.service1.instance1.container import Service1Provider
from src.service2.instance1.container import Service2Provider

# Step 2: container injection
from src.inject import inject
inject({"config": True})