from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class FlightResponse(BaseModel):
    carrier_id: str = Field(..., description='ID авиакомпании')
    carrier_name: str = Field(..., description='Название авиакомпании')
    flight_number: str = Field(..., description='Номер рейса')
    source: str = Field(..., description='Аэропорт отправления (IATA код)')
    destination: str = Field(..., description='Аэропорт прибытия (IATA код)')
    departure_timestamp: Optional[str] = Field(None, description='Время отправления в формате ISO')
    arrival_timestamp: Optional[str] = Field(None, description='Время прибытия в формате ISO')
    class_code: str = Field(..., description='Класс обслуживания')
    number_of_stops: int = Field(..., description='Количество пересадок')
    ticket_type: str = Field(..., description='Тип билета')

    class Config:
        json_schema_extra = {
            'example': {
                'carrier_id': 'AI',
                'carrier_name': 'Air India',
                'flight_number': 'AI-123',
                'source': 'DXB',
                'destination': 'BKK',
                'departure_timestamp': '2024-01-15T10:30:00',
                'arrival_timestamp': '2024-01-15T18:45:00',
                'class_code': 'Y',
                'number_of_stops': 0,
                'ticket_type': 'E',
            }
        }


class ItineraryResponse(BaseModel):
    onward_flights: List[Dict[str, Any]] = Field(..., description='Список рейсов туда')
    return_flights: List[Dict[str, Any]] = Field(..., description='Список рейсов обратно')
    source: str = Field(..., description='Аэропорт отправления (IATA код)')
    destination: str = Field(..., description='Аэропорт прибытия (IATA код)')
    total_duration_minutes: int = Field(..., description='Общая длительность перелёта в минутах')
    total_price: float = Field(..., description='Общая цена перелёта')
    currency: str = Field(..., description='Валюта цены')
    pricing: Dict[str, Any] = Field(..., description='Детальная информация о ценообразовании')

    class Config:
        json_schema_extra = {
            'example': {
                'onward_flights': [
                    {
                        'carrier_id': 'AI',
                        'carrier_name': 'Air India',
                        'flight_number': 'AI-123',
                        'source': 'DXB',
                        'destination': 'BKK',
                        'departure_timestamp': '2024-01-15T10:30:00',
                        'arrival_timestamp': '2024-01-15T18:45:00',
                        'class_code': 'Y',
                        'number_of_stops': 0,
                        'ticket_type': 'E',
                    }
                ],
                'return_flights': [],
                'source': 'DXB',
                'destination': 'BKK',
                'total_duration_minutes': 495,
                'total_price': 450.50,
                'currency': 'USD',
                'pricing': {
                    'currency': 'USD',
                    'total_adult': 450.50,
                    'service_charges': {},
                },
            }
        }


class ComparisonResponse(BaseModel):
    only_in_first: List[Dict[str, Any]] = Field(
        ..., description='Перелёты, присутствующие только в первом запросе'
    )
    only_in_second: List[Dict[str, Any]] = Field(
        ..., description='Перелёты, присутствующие только во втором запросе'
    )
    price_changes: List[Dict[str, Any]] = Field(
        ..., description='Перелёты с изменёнными ценами между запросами'
    )
    total_first: int = Field(..., description='Общее количество перелётов в первом запросе')
    total_second: int = Field(..., description='Общее количество перелётов во втором запросе')

    class Config:
        json_schema_extra = {
            'example': {
                'only_in_first': [],
                'only_in_second': [],
                'price_changes': [],
                'total_first': 10,
                'total_second': 12,
            }
        }
