# Step 1: Providers injection
from src.service1.instance.container import Service1InstanceProvider
from src.service2.instance.container import Service2InstanceProvider

# Step 2: container injection
from src.inject import Container