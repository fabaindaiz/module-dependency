# module-injection

This repository contains experiments and examples for managing dependencies using dependency injection with class decorators in Python projects. The structures and patterns demonstrated here are flexible and can be adapted to suit various project needs.

## Overview

The goal of this project is to showcase different approaches to dependency management, focusing on modularity, flexibility, and ease of use. While the provided examples are specific, the underlying concepts can be applied to a wide range of scenarios.

## Core Components

The project is built around four components that implement different aspects of dependency management:

### 1. Module
- Acts as a container for organizing and grouping related dependencies
- Facilitates modular design and hierarchical structuring of application components

```python
from dependency.core import ProviderModule, module
from plugin........component import SomeService, SomeServiceComponent

@module(
    declaration=[   # Declare all components that are part of the module
        SomeServiceComponent,
        ...         # Every used component must be declared in some module
    ],
    bootstrap=[     # Bootstrap components will be started on loading
        SomeServiceComponent
    ]
)
class SomeModule(ProviderModule):
    """This is a module class.
       Here the providers are declared and provided
    """
    def declare_providers(self): # type: ignore
        from plugin........provider import ImplementedSomeService
        return [    # Here you declare the providers for the components
            ImplementedSomeService,
            ...     # Only one provider per component is allowed
        ]
```

### 2. Component
- Defines abstract interfaces or contracts for dependencies
- Promotes loose coupling and enables easier testing and maintenance

```python
from abc import ABC, abstractmethod
from dependency.core import Component, component

class SomeService(ABC):
    """This is the interface for a new component."""
    @abstractmethod
    def method(self, ...) -> ...:
        pass

@component(
    interface=SomeService, # Declares the interface used by the component
)
class SomeServiceComponent(Component):
    """This is the component class.
       Provider selected for this component will injected here.
       Components are only started when provided or bootstrapped.
    """
    pass
```

### 3. Provider
- Delivers concrete implementations of Components
- Manages the lifecycle and injection of dependency objects

```python
from dependency_injector import providers
from dependency.core import provider
from plugin........component import SomeService, SomeServiceComponent
from plugin..other_component import OtherService, OtherServiceComponent

@provider(
    component=SomeServiceComponent, # Declares the component to be provided
    imports=[OtherService, ...],    # List of dependencies (components) that are needed
    provider=providers.Singleton    # Provider type (Singleton, Factory)
)
class ImplementedSomeService(SomeService):
    """This is a provider class. Here the component is implemented.
       Providers are injected into the respective components when provided.
    """
    def __init__(self, cfg: dict, **kwargs) -> None:
        """Init method will be called when the provider is stared.
           This will happen once for singleton and every time for factories.
        """

        # Once declared, i can use the dependencies for the class.
        self.dependency: OtherService = OtherServiceComponent.provide()
    
    def method(self, ...) -> ...:
        """Methods declared in the interface must be implemented."""
        do_something()
```

## 4. Dependent
- Represents a class produced by a Provider that requires dependencies
- Allows to provide standalone classed without the need to define new providers

```python
from dependency.core import Dependent, dependent

@dependent(
    imports=[SomeComponent, ...], # List of dependencies (components) that are needed
)
class SomeDependent(Interface, Dependent):
    """This is the dependent class.
       Dependents must be declared in the provider that provides them.
       Dependents can be instantiated without the need to define new providers.
    """
    def method(self, ...) -> ...:
        pass
```

These components work together to create a powerful and flexible dependency injection system, allowing for more maintainable and testable Python applications.

## Usage Examples

This repository includes a practical example demonstrating how to use the framework. You can find this example in the `example` directory. It showcases the implementation of the core components and how they interact to manage dependencies effectively in a sample application.

## Future Work

This project is a work in progress, and there are several improvements and enhancements planned for the future. Some of the areas that will be explored include:
- Improve component registration and resolution mechanisms
- Improve ways to handle module definitions and configurations
- Explore more advanced dependency injection patterns and use cases
- Enhance validation and error handling mechanisms of the framework

## Aknowledgements

This project depends on [dependency-injector](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html). This library provides a robust and flexible framework for managing dependencies in Python projects.