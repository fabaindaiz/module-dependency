"""A unit built without a screen.

This is what `optional=` buys, and it is the example's central claim. Declaration is a
process-global side effect, so a station without the display plugin cannot be built in
the same interpreter as one with it — the honest test is a subprocess.
"""
import subprocess
import sys
import textwrap
from example.plugin.display.panel import StatusPanel
from example.plugin.telemetry.alerts.console import ConsoleAlertSink

HEADLESS = textwrap.dedent("""
    import logging
    logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
    from dependency.core import Container, Entrypoint
    from example.app.main import DEFAULT_CONFIG
    from example.plugin.runtime import RuntimePlugin
    from example.plugin.sensors import SensorsPlugin
    from example.plugin.sensors.sampler import Sampler
    from example.plugin.storage import StoragePlugin
    from example.plugin.storage.store import ReadingStore
    from example.plugin.telemetry import TelemetryPlugin

    class HeadlessStation(Entrypoint):
        def __init__(self):
            super().__init__(
                Container.from_json(str(DEFAULT_CONFIG), required=True),
                [RuntimePlugin, SensorsPlugin, StoragePlugin, TelemetryPlugin],
            )
            import example.plugin.runtime.imports
            import example.plugin.sensors.imports
            import example.plugin.storage.imports
            import example.plugin.telemetry.imports
            super().initialize()
            Sampler.provide().warmup()

    HeadlessStation()
    assert ReadingStore.provide().recent(), "the station must have sampled"
    print("HEADLESS-OK")
""")


def test_statuspanel_is_declared_optional_not_required() -> None:
    """The declaration itself, independent of what happens to be resolved.

    Under `imports=` the station would refuse to start on a unit with no screen.
    """
    injection = ConsoleAlertSink.injection
    assert StatusPanel.injection in injection.optional_imports
    assert StatusPanel.injection not in injection.imports


def test_station_boots_and_samples_without_the_display_plugin() -> None:
    result = subprocess.run(
        [sys.executable, "-c", HEADLESS],
        capture_output=True, text=True, cwd="src",
    )
    assert result.returncode == 0, result.stderr
    assert "HEADLESS-OK" in result.stdout
    assert "no status panel on this unit" in result.stderr
