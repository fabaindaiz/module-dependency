"""Container configuration belongs to the Container, not to the process.

The suite's whole isolation boundary is "one `Container` per test" (D-023). These are the
tests that the boundary actually holds for configuration, which it did not: `config` was
assigned in the class body, and `DynamicContainer` does not copy providers per instance.
"""
from dependency.core.resolution import Container

def test_config_is_not_shared_between_containers() -> None:
    first = Container.from_dict({"alpha": 1})
    second = Container.from_dict({"beta": 2})

    assert first.config is not second.config
    assert first.config() == {"alpha": 1}
    assert second.config() == {"beta": 2}

def test_config_is_a_provider_of_its_container() -> None:
    container = Container.from_dict({"alpha": 1})

    assert "config" in container.providers
