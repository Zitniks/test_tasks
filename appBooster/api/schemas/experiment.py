from pydantic import BaseModel


class ExperimentResponse(BaseModel):
    button_color: str | None = None
    price: str | None = None


class StatisticsResponse(BaseModel):
    experiment_key: str
    total_devices: int
    distribution: dict
