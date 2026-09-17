# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.0] - 2026-09-17

**Breaking.** `Registry` was removed from the public API (`dependency.core.__all__`) and
replaced by the expansion result types — `ExpansionFailure` and `ExpansionResult`. Under
semantic versioning that is a major release, and this is it.

### Added

- **The `dependency` command.** `check` expands and resolves a graph without wiring or
  bootstrapping it, so it is safe in CI, and prints the same import chains a failed startup
  would; `show` prints the injection tree with each bound implementation; `graph` renders
  it to SVG; `new plugin|module|component|instance` scaffolds a file. Built on `argparse`,
  so it adds no dependency
- **A pytest plugin**, `pip install module-dependency[testing]`. Registers itself through
  the `pytest11` entry point and provides a `dependency_container` fixture. Nothing is
  autouse, so installing it changes no existing behaviour
- `Entrypoint.shutdown()` and `ResolutionStrategy.shutdown()`: the framework now tears down
  its own `Resource` providers, in reverse of the order it started them. Applications used
  to have to walk the injection tree by hand, because the root container cannot reach
  providers living in plugin sub-containers
- `ProviderExpansion`: dependency graph expansion as an explicit four-step breadth-first
  walk, reporting `ExpansionResult` with both resolved providers and failures
- `ExpansionFailure` and `ExpansionResult` are now public, carrying the full import chain
  (`A -> B -> C`) for every provider that could not enter resolution
- Optional imports via `optional=` on `@component`, `@instance` and `@product`: followed
  when implemented, skipped silently otherwise, and never cascading a failure
- `[graph]` optional extra for dependency graph rendering: `pip install module-dependency[graph]`
- `dependency.library.components`: reusable, **undecorated** `Component` contracts with
  their implementation mixins — `ObserverComponent`, `CompositeComponent` and
  `StateComponent`. The application applies `@component` and `@instance` itself, so the
  module, provider, imports and domain types stay where the domain is
- Agent instruction system: `CLAUDE.md`, area guides, skills, `docs/decisions.md`,
  `docs/references.md`, `docs/roadmap.md`
- `tools/audit_dependency.py`, twelve structural checks, wired into `hatch run build:gate`

### Changed

- **Bootstrap runs in dependency order.** A provider's required imports bootstrap before
  it, and components ready together run in name order. Previously the framework iterated a
  `set`, so the order was unspecified
- **Two providers with the same class name under one container now raise** a
  `DeclarationError` instead of silently overwriting each other. Same names under different
  containers are unaffected
- `Container.config` is per instance. It was assigned in the class body and `DynamicContainer`
  does not copy providers per instance, so every container in a process shared one
  configuration object
- `ResolutionStrategy.injection` returns the resolution order instead of `None`;
  `ResolutionStrategy.resolution` and `InjectionResolver.resolve_providers` return a `list`
  in that order instead of a `set`
- `Entrypoint(strategy=...)` defaults to `None` and builds a strategy per instance. The old
  default was evaluated once at import and shared by every `Entrypoint` in the process
- A plugin that declares no `config:` hint no longer warns. A hint that is not a `BaseModel`
  still does, and now says what the consequence is
- **Minimum Python is now 3.12.** The package declared `>=3.11` but used `typing.override`
  (3.12+, PEP 698) and could not be imported on 3.11 at all
- `dependency_injector` is bounded to `>=4.48.2,<5`. 4.48.2 introduced the `warn_unresolved`
  wiring argument the framework relies on
- Orphan providers are adopted into the container of whichever provider first imports them,
  replacing the previous fallback plugin mechanism
- Documentation rewritten against the current code: `docs/architecture.md` replaces
  `docs/ARCHITECTURE.md`, `docs/index.md` replaces the duplicated `docs/README.md`

### Fixed

- `dependency.library.graph` failed to import on Python 3.12 and 3.13 with
  `NameError: name 'Drawable' is not defined` — unquoted forward references in class bodies,
  which only work from 3.14 onward (PEP 649). No test imported the module
- `dependency.library.graph` imported `graphviz`, which was never declared as a dependency,
  so it failed for every user who installed from PyPI
- `hatch run build:graph` called `generate_graph()` without its required `plugins` argument
- The code generator emitted `@component(interface=...)` and `@instance(component=...)`,
  neither of which exists — generated modules raised `TypeError` on import
- Two `mypy --strict` errors that were never caught because CI did not run the type checker

### Removed

- `Composite.getChildren()` is now the `children` property, matching `StateHolder.state`
  and the framework's snake_case convention
- The `if __name__ == '__main__'` demo blocks in `library/patterns/`, superseded by the
  test suite and the example application
- `Registry` and the global registry validation pass, superseded by `ProviderExpansion`
- The internal fallback plugin for orphan providers
- The `[tool.mypy]` block in `pyproject.toml`, which never applied — `.mypy.ini` takes
  precedence, so its pydantic plugin and `mypy_path` had no effect

### Migrating

See [docs/migration.md](docs/migration.md). **There is no deprecation path and there will
not be one** — a major release removes, which is what a major means. What you get instead
is that a removal can never ship silently: the public API is snapshotted and compared on
every build, so a name leaving `dependency.core.__all__` forces a major bump first.

## [v1.1.7] - 2026-05-04

### Fixed

- `ProviderMixin` is now an abstract base class, so a mixin used without its required
  methods fails at declaration rather than at injection
- Abstract base class usage in the example application

## [v1.1.6] - 2026-03-22

### Added

- Dependency graph visualization: `dependency.library.graph.generate_graph` renders the
  resolved injection tree to SVG via graphviz

## [v1.1.5] - 2026-03-20

### Added

- Extensive unit tests for core modules, including resolution strategy, injection, and product management
- Updated documentation with examples and usage guidelines for new features and changes

## [v1.1.4] - 2026-03-19

### Added

- MkDocs configuration for documentation site deployment to GitHub Pages

### Changed

- Updated documentation and docstrings to reflect recent changes and improvements

## [v1.1.3] - 2026-03-16

### Added

- Support for provider classes in LazyWiring, allowing for more flexible and intuitive dependency injection configurations
- Fallback plugin will be used as parent for all orphans injectables, allowing for better handling of unregistered dependencies

### Changed

- LazyWiring now accepts provider classes directly, allowing for more intuitive usage

## [v1.1.2] - 2026-03-16

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
