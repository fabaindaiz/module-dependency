from enum import Enum

class StationMode(Enum):
    """Where the station is in its lifecycle.

    A three-state enum rather than a pair of booleans: of the four combinations two
    would be meaningless, and a state the data cannot express is a state nobody has to
    check for.
    """
    STARTING = "starting"
    SAMPLING = "sampling"
    DEGRADED = "degraded"
    STOPPED = "stopped"
