from fastapi import APIRouter, Depends
from typing import Union

from .enum import City, BusStopSelection, TransportType
from app.configuration.config_variables import writers
from app.utils.utils import optional_parameters, get_data_about_transport, get_busstop_city, get_busstop_transport, bus_stop_data

router = APIRouter()


@router.get("/{city}")
async def get_bus_stop_city(city: City) -> list:
    """ Gives stops to a specific city """
    return get_busstop_city(city)


@router.get("/{city}/{transport_type}/{transport_number}")
async def get_bus_stop_transport(city: City, transport_type: TransportType, transport_number: str) -> Union[str, list]:
    """ Gives information on certain buses of the city """
    return get_busstop_transport(city, transport_type, transport_number)


@router.get("/{city}/{selection_bus_stop}")
async def bus_stop(city: City, selection_bus_stop: BusStopSelection, optional_data: list = Depends(optional_parameters)) -> dict:
    """Gives information about all buses of a certain city"""
    time, sort, time_format = optional_data
    return await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)


@router.get("/{city}/{selection_bus_stop}/{transport_type}/{transport_number}")
async def bus_stop_transport(city: City, selection_bus_stop: BusStopSelection, transport_type: TransportType, transport_number: str,
                             optional_data: list = Depends(optional_parameters)) -> dict:
    """Gives information about a particular bus in a certain city"""
    time, sort, time_format = optional_data
    return await get_data_about_transport(time, city, selection_bus_stop, transport_number, writers, sort, transport_type, time_format)
