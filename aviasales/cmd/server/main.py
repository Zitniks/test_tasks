from pathlib import Path

from fastapi import FastAPI, HTTPException, status

from api.schemas.flight import ComparisonResponse, ItineraryResponse
from configs.settings import settings
from internal.parser.xml_parser import parse_xml_file
from pkg.utils.flights import (
    compare_itineraries,
    filter_flights_by_route,
    find_cheapest,
    find_fastest,
    find_most_expensive,
    find_optimal,
    find_slowest,
)

app = FastAPI(
    title='Aviasales Flight Search API',
    version='1.0.0',
    description='Веб-сервис для анализа данных о перелётах из XML файлов партнёров Aviasales. '
                'Предоставляет API для поиска вариантов перелёта, сравнения цен и анализа маршрутов.',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
    tags_metadata=[
        {
            'name': 'Flights',
            'description': 'Операции для поиска и фильтрации перелётов по маршруту DXB-BKK',
        },
        {
            'name': 'Comparison',
            'description': 'Сравнение результатов двух запросов перелётов',
        },
        {
            'name': 'Health',
            'description': 'Проверка состояния сервиса',
        },
    ],
)

base_dir = Path(__file__).parent.parent.parent
itineraries_1 = []
itineraries_2 = []


@app.on_event('startup')
def startup():
    global itineraries_1, itineraries_2
    
    file1_path = base_dir / settings.xml_file_1
    file2_path = base_dir / settings.xml_file_2
    
    if not file1_path.exists():
        raise FileNotFoundError(f'XML file not found: {file1_path}')
    if not file2_path.exists():
        raise FileNotFoundError(f'XML file not found: {file2_path}')
    
    itineraries_1 = parse_xml_file(str(file1_path))
    itineraries_2 = parse_xml_file(str(file2_path))


@app.get(
    '/api/v1/flights/dxb-bkk',
    response_model=list[ItineraryResponse],
    tags=['Flights'],
    summary='Получить все варианты перелёта DXB-BKK',
    description='Возвращает список всех доступных вариантов перелёта из Дубая (DXB) в Бангкок (BKK)',
    response_description='Список всех вариантов перелёта с информацией о рейсах, ценах и длительности',
)
def get_flights_dxb_bkk():
    filtered = filter_flights_by_route(itineraries_2, 'DXB', 'BKK')
    return [ItineraryResponse(**it.to_dict()) for it in filtered]


@app.get(
    '/api/v1/flights/dxb-bkk/cheapest',
    response_model=ItineraryResponse,
    tags=['Flights'],
    summary='Найти самый дешёвый перелёт DXB-BKK',
    description='Возвращает вариант перелёта с минимальной ценой из Дубая (DXB) в Бангкок (BKK)',
    responses={
        200: {'description': 'Самый дешёвый вариант перелёта найден'},
        404: {'description': 'Перелёты не найдены'},
    },
)
def get_cheapest_dxb_bkk():
    filtered = filter_flights_by_route(itineraries_2, 'DXB', 'BKK')
    cheapest = find_cheapest(filtered)
    if not cheapest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No flights found')
    return ItineraryResponse(**cheapest.to_dict())


@app.get(
    '/api/v1/flights/dxb-bkk/most-expensive',
    response_model=ItineraryResponse,
    tags=['Flights'],
    summary='Найти самый дорогой перелёт DXB-BKK',
    description='Возвращает вариант перелёта с максимальной ценой из Дубая (DXB) в Бангкок (BKK)',
    responses={
        200: {'description': 'Самый дорогой вариант перелёта найден'},
        404: {'description': 'Перелёты не найдены'},
    },
)
def get_most_expensive_dxb_bkk():
    filtered = filter_flights_by_route(itineraries_2, 'DXB', 'BKK')
    most_expensive = find_most_expensive(filtered)
    if not most_expensive:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No flights found')
    return ItineraryResponse(**most_expensive.to_dict())


@app.get(
    '/api/v1/flights/dxb-bkk/fastest',
    response_model=ItineraryResponse,
    tags=['Flights'],
    summary='Найти самый быстрый перелёт DXB-BKK',
    description='Возвращает вариант перелёта с минимальной длительностью из Дубая (DXB) в Бангкок (BKK)',
    responses={
        200: {'description': 'Самый быстрый вариант перелёта найден'},
        404: {'description': 'Перелёты не найдены'},
    },
)
def get_fastest_dxb_bkk():
    filtered = filter_flights_by_route(itineraries_2, 'DXB', 'BKK')
    fastest = find_fastest(filtered)
    if not fastest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No flights found')
    return ItineraryResponse(**fastest.to_dict())


@app.get(
    '/api/v1/flights/dxb-bkk/slowest',
    response_model=ItineraryResponse,
    tags=['Flights'],
    summary='Найти самый долгий перелёт DXB-BKK',
    description='Возвращает вариант перелёта с максимальной длительностью из Дубая (DXB) в Бангкок (BKK)',
    responses={
        200: {'description': 'Самый долгий вариант перелёта найден'},
        404: {'description': 'Перелёты не найдены'},
    },
)
def get_slowest_dxb_bkk():
    filtered = filter_flights_by_route(itineraries_2, 'DXB', 'BKK')
    slowest = find_slowest(filtered)
    if not slowest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No flights found')
    return ItineraryResponse(**slowest.to_dict())


@app.get(
    '/api/v1/flights/dxb-bkk/optimal',
    response_model=ItineraryResponse,
    tags=['Flights'],
    summary='Найти оптимальный перелёт DXB-BKK',
    description='Возвращает оптимальный вариант перелёта, учитывающий баланс между ценой и временем из Дубая (DXB) в Бангкок (BKK)',
    responses={
        200: {'description': 'Оптимальный вариант перелёта найден'},
        404: {'description': 'Перелёты не найдены'},
    },
)
def get_optimal_dxb_bkk():
    filtered = filter_flights_by_route(itineraries_2, 'DXB', 'BKK')
    optimal = find_optimal(filtered)
    if not optimal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No flights found')
    return ItineraryResponse(**optimal.to_dict())


@app.get(
    '/api/v1/flights/compare',
    response_model=ComparisonResponse,
    tags=['Comparison'],
    summary='Сравнить результаты двух запросов',
    description='Сравнивает результаты двух XML запросов и возвращает различия: '
                'перелёты только в первом запросе, только во втором, и изменения цен',
    response_description='Результат сравнения с детализацией различий между запросами',
)
def compare_flights():
    comparison = compare_itineraries(itineraries_1, itineraries_2)
    return ComparisonResponse(**comparison)


@app.get(
    '/api/v1/health',
    tags=['Health'],
    summary='Проверка состояния сервиса',
    description='Возвращает статус работы сервиса и количество загруженных перелётов из XML файлов',
    response_description='Статус сервиса и статистика загруженных данных',
)
def health():
    return {'status': 'ok', 'itineraries_1': len(itineraries_1), 'itineraries_2': len(itineraries_2)}
