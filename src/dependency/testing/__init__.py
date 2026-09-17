"""Testing helpers for applications built with this framework.

Install with the `testing` extra. The pytest plugin registers itself through the
`pytest11` entry point; importing this package is not required to use the fixtures.
"""

from dependency.testing.plugin import declaration_state

__all__ = [
    "declaration_state",
]
