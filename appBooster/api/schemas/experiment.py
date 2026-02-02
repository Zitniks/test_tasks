"""Схемы ответов API экспериментов."""

from pydantic import BaseModel


class ExperimentResponse(BaseModel):
    """Ответ с назначенными значениями экспериментов (ключи = experiment_key)."""

    button_color: str | None = None
    price: str | None = None


class DistributionItem(BaseModel):
    """One option in experiment statistics: count, weight, percentage."""

    count: int
    weight: int
    percentage: float


class StatisticsResponse(BaseModel):
    """Статистика по одному эксперименту: ключ, число устройств, распределение по опциям."""

    experiment_key: str
    total_devices: int
    distribution: dict[str, DistributionItem]
