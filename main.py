import asyncio
import vk_api
from config import login, password

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from utils.write_in_bd_data import Writer
from utils.utils import check_bus, bus_stop_data

from models.database import *
from models.enum import City, BusStopSelection, TransportType

vk = vk_api.VkApi(login=login, password=password)
vk.auth()

app = FastAPI(
    title="AntiContollerApi",
    description="I give you information about controllers in the cities of Belarus",
    version="0.1.2",
    openapi_url="/api/v1/openapi.json"
    )

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

writers = {
    'brest': [BusStopDirty_Brest, BusStopClear_Brest],
    'gomel': [BusStopDirty_Gomel, BusStopClear_Gomel],
    'grodno': [BusStopDirty_Grodno, BusStopClear_Grodno]
}

writer = Writer(vk)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()
    for wr in writers:
        data = writers.get(wr)
        for info in data:
            asyncio.create_task(writer.write_in_database(info))


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.get("/bus_stop/{city}/{selection_bus_stop}")
async def bus_stop(city: City, selection_bus_stop: BusStopSelection, time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    return await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)


@app.get("/bus_stop/{city}/{selection_bus_stop}/{transport_type}/{transport_number}")
async def bus_stop_dirty_bus(city: City, selection_bus_stop: BusStopSelection, transport_type: TransportType, transport_number: str, time: int = 3600, sort: str = 'Время',
                             time_format: str = '%H:%M') -> dict:
    data: dict = await bus_stop_data(time, city, selection_bus_stop, sort, time_format, writers)
    return check_bus(city, transport_type, data, transport_number, sort)
