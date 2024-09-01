# mixin-injection

This repository contains experiments and examples for managing dependencies using dependency injection with mixins in Python projects. The structures and patterns demonstrated here are flexible and can be adapted to suit various project needs.

## Overview

The goal of this project is to showcase different approaches to dependency management, focusing on modularity, flexibility, and ease of use. While the provided examples are specific, the underlying concepts can be applied to a wide range of scenarios.

## Structure

The project is organized into several modules, each demonstrating a different aspect of dependency management:

- services: Demonstrates standalone services that can be used by other providers.
- manager: Shows how to create a manager that merges multiple services into a single service.
- plugin: Illustrates multiple layers of services that can be used by other providers.

## Aknowledgements

This project utilizes the [Dependency Injector](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) library for Python. This powerful library provides a robust and flexible framework for managing dependencies in Python projects.