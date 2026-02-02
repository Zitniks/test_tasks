from pydantic import BaseModel


class ExperimentResponse(BaseModel):
    button_color: str | None = None
    price: str | None = None


class DistributionItem(BaseModel):
    """One option in experiment statistics: count, weight, percentage."""

    count: int
    weight: int
    percentage: float


class StatisticsResponse(BaseModel):
    experiment_key: str
    total_devices: int
    distribution: dict[str, DistributionItem]
