from typing import List, Optional

from internal.models.flight import FlightItinerary


def filter_flights_by_route(itineraries: List[FlightItinerary], source: str, destination: str) -> List[FlightItinerary]:
    return [it for it in itineraries if it.get_source() == source and it.get_destination() == destination]


def find_cheapest(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    if not itineraries:
        return None
    return min(itineraries, key=lambda x: x.get_total_price())


def find_most_expensive(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    if not itineraries:
        return None
    return max(itineraries, key=lambda x: x.get_total_price())


def find_fastest(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    if not itineraries:
        return None
    return min(itineraries, key=lambda x: x.get_total_duration_minutes())


def find_slowest(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    if not itineraries:
        return None
    return max(itineraries, key=lambda x: x.get_total_duration_minutes())


def find_optimal(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    if not itineraries:
        return None
    
    def score(it: FlightItinerary) -> float:
        price = it.get_total_price()
        duration = it.get_total_duration_minutes()
        if price == 0 or duration == 0:
            return float('inf')
        return (price / 100.0) + (duration / 10.0)
    
    return min(itineraries, key=score)


def compare_itineraries(itineraries1: List[FlightItinerary], itineraries2: List[FlightItinerary]) -> dict:
    def get_itinerary_key(it: FlightItinerary) -> str:
        flights_str = '_'.join([f"{f.source}-{f.destination}" for f in it.onward_flights])
        return f"{it.get_source()}-{it.get_destination()}_{flights_str}_{it.get_total_price()}"
    
    keys1 = {get_itinerary_key(it): it for it in itineraries1}
    keys2 = {get_itinerary_key(it): it for it in itineraries2}
    
    only_in_1 = [it.to_dict() for key, it in keys1.items() if key not in keys2]
    only_in_2 = [it.to_dict() for key, it in keys2.items() if key not in keys1]
    
    common = []
    for key in keys1:
        if key in keys2:
            it1 = keys1[key]
            it2 = keys2[key]
            if it1.get_total_price() != it2.get_total_price():
                common.append({
                    'itinerary': it1.to_dict(),
                    'price_changed': {
                        'old': it1.get_total_price(),
                        'new': it2.get_total_price(),
                    }
                })
    
    return {
        'only_in_first': only_in_1,
        'only_in_second': only_in_2,
        'price_changes': common,
        'total_first': len(itineraries1),
        'total_second': len(itineraries2),
    }
