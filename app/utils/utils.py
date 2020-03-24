from time import time as tm
from typing import Union

from .db import get_city_data
from .validation import sort_busstop
from app.configuration.config_variables import list_bus_stop


def optional_parameters(time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M'):
    return time, sort, time_format


def get_stop_city(city: str) -> list:
    bus_stops_dict: list = get_busstop_city(city)
    bus_stop = []
    for bus_stop_dict in bus_stops_dict:
        for bus_stop_list in bus_stop_dict.values():
            bus_stop.append(bus_stop_list[0])
    return list(set(bus_stop))


def get_transport_stop(city: str, type_transport: str) -> dict:
    transport_stop: list = list_bus_stop.get(city)
    if type_transport == 'bus':
        transport_stop: dict = transport_stop[0]
    else:
        transport_stop: dict = transport_stop[1]
    return transport_stop


def get_transport_number_city(city: str, type_transport: str):
    return get_transport_stop(city, type_transport).keys()


def get_busstop_transport(city: str, type_transport: str, transport_number: str) -> Union[str, list]:
    bus_stop: list = get_transport_stop(city, type_transport).get(transport_number)
    if not bus_stop:
        return f"{transport_number} is not in the database"
    return bus_stop


def get_busstop_city(city: str):
    return list_bus_stop.get(city)


def check_bus(city: str, type_bus: str, data: dict, bus_number: str, sort: str) -> dict:
    """ Поиск грязных остановок в остановках автобуса """
    bus_stop_list = list_bus_stop.get(city)
    json_utils: dict = {}
    if bus_stop_list:
        json_utils: dict = bus_stop_list[0] if type_bus == 'bus' else bus_stop_list[1]
    _bus_stop: list = json_utils.get(bus_number)
    if not _bus_stop:
        return {'number_bus_not_found': [bus_number, 228]}

    temporary_lists: list = []
    for stop in _bus_stop:
        for datas in data:
            if datas == stop.lower():
                _data = data.get(datas)
                temporary_lists.append((datas, [_data[0], _data[1]]))

    _sort: int = 1
    if sort == "Сообщения":
        _sort: int = 0
    return dict(sorted(dict(temporary_lists).items(), key=lambda x: x[1][_sort], reverse=True))


async def bus_stop_data(time: int, city: str, selection_bus_stop: str, sort: str, time_format: str, writers: dict) -> dict:
    unix_time: int = int(tm()) - time
    data: list = await get_city_data(city, selection_bus_stop, unix_time, writers)
    return sort_busstop(data=data, _sort=sort, time_format=time_format)


async def get_data_about_transport(time: int, city: str, selection_bus_stop: str, transport_number: str, writers: dict, sort: str,
                                   type_transport: str, time_format: str) -> dict:
    data: dict = await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)
    return check_bus(city, type_transport, data, transport_number, sort)
