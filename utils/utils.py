from sqlalchemy import desc
from configuration.config_variables import list_bus_stop
from time import time as tm
from .validation import sort_busstop


async def get_max_value_bd(model, value):
    selection = model.objects.build_select_expression().order_by(desc(value))
    max_value_bd = await model.__database__.execute(selection)
    response = await model.objects.get(id=max_value_bd)
    return response[value]


async def get_city_data(city: str, type_geter: str, _time: int, writers: dict):
    city = city.lower()
    db_class = writers.get(city)
    if not db_class:
        return [{'bus_stop': 'Wrong city', 'time': 228}]
    elif type_geter == 'dirty':
        return await db_class[0].objects.filter(time__gte=_time).all()
    elif type_geter == 'clean':
        return await db_class[1].objects.filter(time__gte=_time).all()


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
    data: tuple = await get_city_data(city, selection_bus_stop, unix_time, writers)
    return sort_busstop(data=data, _sort=sort, time_format=time_format)
