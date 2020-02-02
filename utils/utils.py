from sqlalchemy import desc
from config import list_bus_stop
from time import time as tm
from .validation import sort_busstop

async def get_max_value_bd(model, value):
    selection = model.objects.build_select_expression().order_by(desc(value))
    max_value_bd = await model.__database__.execute(selection)
    response = await model.objects.get(id=max_value_bd)
    return response[value]

async def get_valid_city(city: str, type_geter: str, _time: int, writers):
    city = city.lower()
    db_class = writers.get(city)
    if not db_class:
        return [{'bus_stop': 'Wrong city', 'time': 228}]
    elif type_geter == 'dirty':
        return await db_class[0].objects.filter(time__gte=_time).all()
    elif type_geter == 'clean':
        return await db_class[1].objects.filter(time__gte=_time).all()

def check_bus(city, type_bus: str, data, bus_number, sort: str):
    """ Поиск грязных остановок в остановках автобуса """

    json_utils = list_bus_stop.get(city)[0] if type_bus == 'bus' else list_bus_stop.get(city)[1]
    _bus_stop = json_utils.get(bus_number)
    if not _bus_stop:
        return {'number_bus_not_found': bus_number}

    temporary_lists = []
    for stop in _bus_stop:
        for datas in data:
            _data = data.get(datas)
            if datas == stop.lower():
                t = (datas, [_data[0], _data[1]])
                temporary_lists.append(t)

    _sort = 1
    if sort == "Сообщения":
        _sort = 0
    return dict(sorted(dict(temporary_lists).items(), key=lambda x: x[1][_sort], reverse=True))

async def create_transport_info(writers: dict, sort: str, time_format: str, bus_number: str, time: int, city: str, type_sort: str, type_transport: str) -> dict:
    _time = int(tm()) - time
    datas = await get_valid_city(city, type_sort, _time, writers)
    data = sort_busstop(datas, _sort=sort, time_format=time_format)
    _data = check_bus(city, type_transport, data, bus_number, sort)
    return _data
