from pydantic import BaseModel


class TelemetrySettings(BaseModel):
    alert_prefix: str = "ALERT"


class TelemetryConfig(BaseModel):
    telemetry: TelemetrySettings = TelemetrySettings()
