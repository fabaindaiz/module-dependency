# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.1.3] - 2026-02-

### Added

-

### Changed

- LazyWiring now accepts provider classes directly, allowing for more intuitive usage

## [v1.1.2] - 2026-02-

### Added

- Global registry for managing and validating injectables and providers has been implemented

## [v1.1.1] - 2026-02-20

### Added

- Global registry for managing and validating injectables and providers

### Changed

- Updated documentation and examples to reflect recent changes
- Injectables have been extracted from Injection and now are handled by Providers
- Refactored resolution logic to use a registry for better management and validation
- On components, products declaration has been removed, use imports declaration

## [v1.1.0] - 2026-02-13

### Fixed

- Fixed Products not being exported from the package

## [v1.0.0] - 2026-02-13

### Added

- Components can now implicitly provide products without explicit declaration
- New warning log with helpful message when a non-standard configuration is detected
- Mixin definition for container and provider class parameter and methods
- Resolution Strategy configuration for customizable resolution behavior

### Changed

- Update examples and documentation to reflect recent changes
- Components now can be standalone be implemented by other classes
- Update error messages in logging and exceptions for better clarity
- Updated docstrings for utility classes and methods in core modules
- Separated initialization logic into separate methods for better clarity
- Component & Module classes now use class attributes and methods directly
- Decorators refactored to use classes directly without instantiating or casting

### Removed

- Remove Product class for simplicity, now all providable classes are Components
- Removed abstract base classes for Module, Component & Instance due to refactoring
- Removed Instance class and redundant type hint casts in decorators

## [v0.4.9] - 2025-12-23

### Added

- Lazy Markers for deferred resolution of injection references with @inject decorator
- Meta functions for dynamic injection resolution and internal behavior modification

### Changed

- Prefer use of LazyProvide over Provide for dependency injection for compatibility with meta functions

## [v0.4.8] - 2025-12-18

### Fixed

- Corrected import handling in provider injectable resolution

## [v0.4.7] - 2025-12-18

### Changed

- Refactored injectable definition and resolution logic
- Products are now injected like a normal dependency
- Improved code readability and maintainability
- Updated type hints for class decorators

### Removed

- Removed redundant wiring logic on injection resolution

## [v0.4.6] - 2025-11-27

### Added

- Stubs for dependency and library modules

### Fixed

- Removed unused casts for class decorators in type hints

## [v0.4.5] - 2025-10-27

## [v0.4.3] - 2025-08-11

### Added

- Allow @inject based dependency injection
- New circular dependency detection and handling

### Fixed

- Fixed issues with module decorator typing

### Changed

- Plugin config now retrieved from class type hint
- Improved dependency resolution and injection process

## [v0.4.0] - 2025-08-09

### Added

- New plugin system for better modularity
- Support for dynamic configuration loading
- Updated documentation for plugin development

### Changed

- Improved dependency resolution and injection process
