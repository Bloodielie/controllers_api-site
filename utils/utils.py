from sqlalchemy import desc
from config import list_bus_stop
from time import time as tm
from .validation import sort_busstop


async def get_max_value_bd(model, value):
    selection = model.objects.build_select_expression().order_by(desc(value))
    max_value_bd = await model.__database__.execute(selection)
    response = await model.objects.get(id=max_value_bd)
    return response[value]


async def get_valid_city(city: str, type_geter: str, _time: int, writers: dict):
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
    json_utils = {}
    if bus_stop_list:
        json_utils = bus_stop_list[0] if type_bus == 'bus' else bus_stop_list[1]
    _bus_stop = json_utils.get(bus_number)
    if not _bus_stop:
        return {'number_bus_not_found': [bus_number, 228]}

    temporary_lists = []
    for stop in _bus_stop:
        for datas in data:
            if datas == stop.lower():
                _data = data.get(datas)
                t = (datas, [_data[0], _data[1]])
                temporary_lists.append(t)

    _sort = 1
    if sort == "Сообщения":
        _sort = 0
    return dict(sorted(dict(temporary_lists).items(), key=lambda x: x[1][_sort], reverse=True))


class TransportInformation:
    def __init__(self, writers):
        self.writers = writers

    async def __create_transport_info(self, sort: str, time_format: str, bus_number: str, time: int, city: str, type_sort: str, type_transport: str) -> dict:
        _time: int = int(tm()) - time
        datas = await get_valid_city(city, type_sort, _time, self.writers)
        data: dict = sort_busstop(datas, _sort=sort, time_format=time_format)
        return check_bus(city, type_transport, data, bus_number, sort)

    async def create_bus_info(self, sort: str, time_format: str, bus_number: str, time: int, city: str, type_sort: str) -> dict:
        return await self.__create_transport_info(sort, time_format, bus_number, time, city, type_sort, 'bus')

    async def create_trolleybus_info(self, sort: str, time_format: str, bus_number: str, time: int, city: str, type_sort: str) -> dict:
        return await self.__create_transport_info(sort, time_format, bus_number, time, city, type_sort, 'trolleybus')
