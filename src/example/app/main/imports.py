# The set of implementations this build runs with.
#
# Every @instance registers itself at import time, so this file *is* the configuration
# of which implementation wins. Swapping a station to a manual clock, or to disk-backed
# storage, is an edit here and nowhere else.
import example.plugin.runtime.imports
import example.plugin.sensors.imports
import example.plugin.storage.imports
import example.plugin.telemetry.imports
import example.plugin.display.imports
