"""The `dependency` command: exit codes, and the diagnostics it is for.

`check` exists to answer the framework's own question from a shell — does this graph hold
— so the two failure paths matter more than the happy one. A verification command that
exits 0 when nothing was registered is worse than no command at all.
"""

from pathlib import Path
import subprocess
import sys

import pytest

from dependency.cli.main import main

EXAMPLE = "example.app.main.plugins:PLUGINS"
REGISTRATIONS = "example.app.main.imports"
CONFIG = str(Path(__file__).resolve().parents[2] / "src" / "example" / "config.json")


def test_version_prints_the_installed_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["version"]) == 0

    assert capsys.readouterr().out.strip()


def test_new_plugin_writes_a_declaration_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["new", "plugin", "Weather"]) == 0

    out = capsys.readouterr().out
    assert "class Weather(Plugin)" in out
    assert "class WeatherConfig(BaseModel)" in out


def test_new_component_derives_the_interface_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["new", "component", "Clock", "--module", "app.plugin:AppPlugin"]) == 0

    out = capsys.readouterr().out
    assert "class ClockInterface(ABC)" in out
    assert "class Clock(ClockInterface, Component)" in out


def test_new_instance_injects_the_imports_it_was_given(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["new", "instance", "SystemClock", "--component", "app.clock:Clock",
                 "--imports", "Settings"]) == 0

    assert "Settings.provide()" in capsys.readouterr().out


def test_output_flag_writes_a_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    target = tmp_path / "weather.py"

    assert main(["new", "plugin", "Weather", "-o", str(target)]) == 0

    assert "class Weather(Plugin)" in target.read_text()
    assert capsys.readouterr().out == ""


def test_check_resolves_the_example_application(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check", EXAMPLE, "-i", REGISTRATIONS, "-c", CONFIG]) == 0

    assert "provider(s) resolved across 5 plugin(s)" in capsys.readouterr().out


def test_check_fails_when_no_implementation_was_registered() -> None:
    """The dangerous false pass: an empty graph expands cleanly and proves nothing.

    In a subprocess, and not for neatness. Declaration is a process-global import-time side
    effect with no teardown, so any earlier test that imported the registrations leaves them
    registered for every later one — this assertion is only true in a clean interpreter.
    """
    finished = subprocess.run(
        [sys.executable, "-m", "dependency.cli.main", "check", EXAMPLE, "-c", CONFIG],
        capture_output=True,
        text=True,
        check=False,
    )

    assert finished.returncode == 1
    assert "no provider resolved" in finished.stderr


def test_check_rejects_a_spec_that_is_not_module_colon_attribute(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["check", "example.app.main.plugins"]) == 1

    assert "module:attribute" in capsys.readouterr().err


def test_check_reports_an_unimportable_entrypoint(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check", "nosuchpackage.plugins:PLUGINS"]) == 1

    assert "cannot import" in capsys.readouterr().err


def test_check_rejects_an_attribute_that_is_not_a_plugin(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["check", "example.app.main.plugins:__doc__"]) == 1

    assert "Plugin subclass" in capsys.readouterr().err

def test_check_rejects_an_iterable_of_things_that_are_not_plugins(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["check", "example.app.main.plugins:__name__"]) == 1

    assert "not a Plugin subclass" in capsys.readouterr().err


def test_check_reports_a_missing_config_file(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check", EXAMPLE, "-i", REGISTRATIONS, "-c", "/nonexistent.json"]) == 1

    assert "nonexistent.json" in capsys.readouterr().err


def test_show_marks_every_provider_with_its_implementation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["show", EXAMPLE, "-i", REGISTRATIONS, "-c", CONFIG]) == 0

    out = capsys.readouterr().out
    assert "SensorsPlugin/" in out
    assert "[ok] Clock -> SystemClock" in out
