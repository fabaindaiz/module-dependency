"""The example application, end to end.

These tests are also the example's own regression guard: if a core API changes,
src/example breaks here before it breaks for a reader.
"""
import pytest
from dataclasses import FrozenInstanceError
from dependency.core.exceptions import CancelInitialization
from example.app.main import MonitoringStation
from example.plugin.display.panel import StatusPanel
from example.plugin.runtime.modes import StationMode
from example.plugin.sensors.group import SensorGroup
from example.plugin.sensors.interfaces import Reading
from example.plugin.sensors.probes.humidity import HumiditySensor
from example.plugin.sensors.probes.pressure import PressureSensor
from example.plugin.sensors.probes.temperature import TemperatureSensor
from example.plugin.storage.store import ReadingStore
from example.plugin.telemetry.alerts import AlertSink
from example.plugin.telemetry.observer import StationObserver


@pytest.fixture(scope="module")
def station() -> MonitoringStation:
    return MonitoringStation()


def test_station_starts(station: MonitoringStation) -> None:
    assert station.state in (StationMode.SAMPLING, StationMode.DEGRADED)


def test_every_declared_component_resolved(station: MonitoringStation) -> None:
    for component in (
        SensorGroup, ReadingStore, StationObserver, AlertSink,
        TemperatureSensor, HumiditySensor, StatusPanel,
    ):
        assert component.injection.is_resolved, f"{component.__name__} unresolved"


def test_absent_probe_cancels_without_failing_the_graph(station: MonitoringStation) -> None:
    """CancelInitialization is how a missing option declines to start.

    The component still resolves — it was declared and implemented — but providing it
    raises, which is the signal SensorGroup uses to leave the channel out.
    """
    assert PressureSensor.injection.is_resolved
    with pytest.raises(CancelInitialization):
        PressureSensor.provide()


def test_group_contains_only_fitted_probes(station: MonitoringStation) -> None:
    group: SensorGroup = SensorGroup.provide()
    channels = {probe.channel for probe in group.children}
    assert channels == {"temperature", "humidity"}
    assert "pressure" not in channels


def test_missing_probe_puts_the_station_in_degraded(station: MonitoringStation) -> None:
    assert station.state is StationMode.DEGRADED


def test_sampling_stores_one_reading_per_fitted_probe(station: MonitoringStation) -> None:
    before = len(ReadingStore.provide().recent(limit=1000))
    station.run(cycles=2)
    after = ReadingStore.provide().recent(limit=1000)
    assert len(after) - before == 2 * 2  # two cycles, two probes


def test_readings_are_immutable(station: MonitoringStation) -> None:
    reading = ReadingStore.provide().recent(limit=1)[0]
    assert isinstance(reading, Reading)
    with pytest.raises(FrozenInstanceError):
        reading.value = 0.0  # type: ignore[misc]


def test_panel_is_wired_when_the_display_plugin_is_loaded(station: MonitoringStation) -> None:
    assert isinstance(StatusPanel.provide(), StatusPanel)
