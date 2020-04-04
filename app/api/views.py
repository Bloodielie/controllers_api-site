from fastapi import APIRouter

from .enum import City, BusStopSelection, TransportType, AllDataParameter
from app.configuration.config_variables import writers
from app.utils.utils import get_data_about_transport, get_busstop_transport, bus_stop_data, get_stop_city, get_transport_number_city

router = APIRouter()


# @router.get("/{city}/get_situation")
# async def bus_stop(city: City,
#                    selection_bus_stop: BusStopSelection,
#                    time: int = 3600,
#                    sort: str = 'Время',
#                    time_format: str = '%H:%M') -> dict:
#     """Gives information about all buses of a certain city"""
#     return await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)


@router.get("/{city}/get_situation/{transport_number_or_all}")
async def get_situation_in_city(city: City,
                                transport_number_or_all: str,
                                selection_bus_stop: BusStopSelection,
                                time: int = 3600,
                                sort: str = 'Время',
                                time_format: str = '%H:%M',
                                transport_type: TransportType = 'bus') -> dict:
    """Gives information about a particular bus in a certain city"""
    if transport_number_or_all == 'all':
        return await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)
    else:
        return await get_data_about_transport(time, city, selection_bus_stop, transport_number_or_all, writers, sort, transport_type,
                                              time_format)


@router.get("/{city}/{type_information}")
async def get_diverse_data(city: City, type_information: AllDataParameter, transport_type: TransportType = 'bus',
                           transport_number: str = '12') -> list:
    if type_information == AllDataParameter.city_stops.value:
        return get_stop_city(city)
    elif type_information == AllDataParameter.transport_numbers.value:
        return list(get_transport_number_city(city, transport_type))
    elif type_information == AllDataParameter.transport_stops.value:
        return get_busstop_transport(city, transport_type, transport_number)

# @router.get("/{city}/{transport_type}/{transport_number}")
# async def get_bus_stop_transport(city: City, transport_type: TransportType, transport_number: str) -> Union[str, list]:
#     """ Gives information on certain buses of the city """
#     return get_busstop_transport(city, transport_type, transport_number)
