import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional

from internal.models.flight import Flight, FlightItinerary, Pricing


def parse_xml_file(file_path: str) -> List[FlightItinerary]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    itineraries = []
    
    for flights_elem in root.findall('.//PricedItineraries/Flights'):
        onward_elem = flights_elem.find('OnwardPricedItinerary')
        return_elem = flights_elem.find('ReturnPricedItinerary')
        pricing_elem = flights_elem.find('Pricing')
        
        onward_flights = []
        if onward_elem is not None:
            flights_list = onward_elem.find('Flights')
            if flights_list is not None:
                for flight_elem in flights_list.findall('Flight'):
                    flight_data = _parse_flight_element(flight_elem)
                    onward_flights.append(Flight(flight_data))
        
        return_flights = []
        if return_elem is not None:
            flights_list = return_elem.find('Flights')
            if flights_list is not None:
                for flight_elem in flights_list.findall('Flight'):
                    flight_data = _parse_flight_element(flight_elem)
                    return_flights.append(Flight(flight_data))
        
        pricing = None
        if pricing_elem is not None:
            pricing_data = _parse_pricing_element(pricing_elem)
            pricing = Pricing(pricing_data)
        
        if onward_flights:
            itinerary = FlightItinerary(onward_flights, return_flights, pricing)
            itineraries.append(itinerary)
    
    return itineraries


def _parse_flight_element(flight_elem) -> dict:
    data = {}
    
    carrier_elem = flight_elem.find('Carrier')
    if carrier_elem is not None:
        data['Carrier'] = {
            '@id': carrier_elem.get('id', ''),
            '#text': carrier_elem.text or ''
        }
    
    for tag in ['FlightNumber', 'Source', 'Destination', 'DepartureTimeStamp', 
                'ArrivalTimeStamp', 'Class', 'NumberOfStops', 'TicketType']:
        elem = flight_elem.find(tag)
        if elem is not None:
            data[tag] = elem.text or ''
    
    return data


def _parse_pricing_element(pricing_elem) -> dict:
    data = {
        '@currency': pricing_elem.get('currency', ''),
        'ServiceCharges': []
    }
    
    for charge_elem in pricing_elem.findall('ServiceCharges'):
        charge_data = {
            '@type': charge_elem.get('type', ''),
            '@ChargeType': charge_elem.get('ChargeType', ''),
            '#text': charge_elem.text or '0'
        }
        data['ServiceCharges'].append(charge_data)
    
    return data
