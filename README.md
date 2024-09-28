# module-injection

This repository contains experiments and examples for managing dependencies using dependency injection with class decorators in Python projects. The structures and patterns demonstrated here are flexible and can be adapted to suit various project needs.

## Overview

The goal of this project is to showcase different approaches to dependency management, focusing on modularity, flexibility, and ease of use. While the provided examples are specific, the underlying concepts can be applied to a wide range of scenarios.

## Core Components

The project is built around three core components that implement different aspects of dependency management:

### 1. Module
- Acts as a container for organizing and grouping related dependencies
- Facilitates modular design and hierarchical structuring of application components

### 2. Component
- Defines abstract interfaces or contracts for dependencies
- Promotes loose coupling and enables easier testing and maintenance

### 3. Provider
- Delivers concrete implementations of Components
- Manages the lifecycle and injection of dependency objects

These components work together to create a powerful and flexible dependency injection system, allowing for more maintainable and testable Python applications.

## Usage Examples

This repository includes a practical example demonstrating how to use the framework. You can find this example in the `example` directory. It showcases the implementation of the core components and how they interact to manage dependencies effectively in a sample application.

## Aknowledgements

This project depends on [dependency-injector](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html). This library provides a robust and flexible framework for managing dependencies in Python projects.