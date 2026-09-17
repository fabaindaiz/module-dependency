from pydantic import BaseModel

class SensorsSettings(BaseModel):
    """Settings the sensors plugin reads from the application config."""
    sample_interval_s: float = 1.0
    warmup_samples: int = 2
    thresholds: dict[str, float] = {}

class SensorsConfig(BaseModel):
    sensors: SensorsSettings = SensorsSettings()
