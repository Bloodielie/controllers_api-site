from fastapi import APIRouter
from models.enum import City, BusStopSelection, TransportType
from utils.utils import check_bus, bus_stop_data
from configuration.config_variables import writers

router = APIRouter()


@router.get("/{city}/{selection_bus_stop}")
async def bus_stop(city: City, selection_bus_stop: BusStopSelection, time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    return await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)


@router.get("/{city}/{selection_bus_stop}/{transport_type}/{transport_number}")
async def bus_stop_transport(city: City, selection_bus_stop: BusStopSelection, transport_type: TransportType, transport_number: str, time: int = 3600, sort: str = 'Время',
                             time_format: str = '%H:%M') -> dict:
    data: dict = await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)
    return check_bus(city, transport_type, data, transport_number, sort)
