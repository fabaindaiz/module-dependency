"""Load the framework's own pytest plugin from the source tree.

Users get `dependency.testing.plugin` through the `pytest11` entry point, which lives in
the metadata of an **installed** distribution. This suite runs against `PYTHONPATH=src`,
where that metadata is not what is being tested, so the plugin is named here explicitly.

The two mechanisms are deliberately separate: this file proves the fixtures work, and the
`release` skill proves the entry point registers, by installing the built wheel into a
clean venv and loading it there. A repository that only ever tested the first would ship a
plugin that nobody's pytest ever finds.
"""
pytest_plugins = ("dependency.testing.plugin",)
