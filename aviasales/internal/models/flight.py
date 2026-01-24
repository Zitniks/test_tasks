from datetime import datetime
from typing import List, Optional


class Flight:
    def __init__(self, data: dict):
        self.carrier_id = data.get('Carrier', {}).get('@id', '')
        self.carrier_name = data.get('Carrier', {}).get('#text', '')
        self.flight_number = data.get('FlightNumber', '')
        self.source = data.get('Source', '')
        self.destination = data.get('Destination', '')
        self.departure_timestamp = self._parse_timestamp(data.get('DepartureTimeStamp', ''))
        self.arrival_timestamp = self._parse_timestamp(data.get('ArrivalTimeStamp', ''))
        self.class_code = data.get('Class', '')
        self.number_of_stops = int(data.get('NumberOfStops', 0))
        self.ticket_type = data.get('TicketType', '')

    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        if not timestamp_str:
            return None
        try:
            return datetime.strptime(timestamp_str, '%Y-%m-%dT%H%M')
        except ValueError:
            return None

    def to_dict(self) -> dict:
        return {
            'carrier_id': self.carrier_id,
            'carrier_name': self.carrier_name,
            'flight_number': self.flight_number,
            'source': self.source,
            'destination': self.destination,
            'departure_timestamp': self.departure_timestamp.isoformat() if self.departure_timestamp else None,
            'arrival_timestamp': self.arrival_timestamp.isoformat() if self.arrival_timestamp else None,
            'class_code': self.class_code,
            'number_of_stops': self.number_of_stops,
            'ticket_type': self.ticket_type,
        }


class Pricing:
    def __init__(self, data: dict):
        self.currency = data.get('@currency', '')
        self.service_charges = {}
        for charge in data.get('ServiceCharges', []):
            charge_type = charge.get('@ChargeType', '')
            charge_value = charge.get('#text', '0')
            passenger_type = charge.get('@type', '')
            key = f'{passenger_type}_{charge_type}'
            try:
                self.service_charges[key] = float(charge_value)
            except ValueError:
                self.service_charges[key] = 0.0

    def get_total_adult(self) -> float:
        return self.service_charges.get('SingleAdult_TotalAmount', 0.0)

    def to_dict(self) -> dict:
        return {
            'currency': self.currency,
            'total_adult': self.get_total_adult(),
            'service_charges': self.service_charges,
        }


class FlightItinerary:
    def __init__(self, onward_flights: List[Flight], return_flights: Optional[List[Flight]] = None, pricing: Optional[Pricing] = None):
        self.onward_flights = onward_flights
        self.return_flights = return_flights or []
        self.pricing = pricing

    def get_source(self) -> str:
        if self.onward_flights:
            return self.onward_flights[0].source
        return ''

    def get_destination(self) -> str:
        if self.onward_flights:
            return self.onward_flights[-1].destination
        return ''

    def get_total_duration_minutes(self) -> int:
        if not self.onward_flights:
            return 0
        first_departure = self.onward_flights[0].departure_timestamp
        last_arrival = self.onward_flights[-1].arrival_timestamp
        if first_departure and last_arrival:
            delta = last_arrival - first_departure
            return int(delta.total_seconds() / 60)
        return 0

    def get_total_price(self) -> float:
        if self.pricing:
            return self.pricing.get_total_adult()
        return 0.0

    def to_dict(self) -> dict:
        return {
            'onward_flights': [f.to_dict() for f in self.onward_flights],
            'return_flights': [f.to_dict() for f in self.return_flights],
            'source': self.get_source(),
            'destination': self.get_destination(),
            'total_duration_minutes': self.get_total_duration_minutes(),
            'total_price': self.get_total_price(),
            'currency': self.pricing.currency if self.pricing else '',
            'pricing': self.pricing.to_dict() if self.pricing else {},
        }
