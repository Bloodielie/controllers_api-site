from fastapi import FastAPI, Path
import vk_api
from config import login, password
import asyncio
from utils.validation import sort_busstop
from time import time as tm
from database import *
from utils.write_in_bd_data import Writer
from starlette.middleware.cors import CORSMiddleware
from utils.utils import get_valid_city, TransportInformation

vk = vk_api.VkApi(login=login, password=password)
vk.auth()
app = FastAPI()

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
transport_utils = TransportInformation(writers)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()
    for wr in writers:
        data = writers.get(wr)
        for info in data:
            asyncio.ensure_future(writer.write_in_database(info))


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.get("/bus_stop/{city}/dirty")
async def bus_stop_dirty(*, city: str = Path(..., title="city for get data"), time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    _time: int = int(tm()) - time
    datas = await get_valid_city(city, 'dirty', _time, writers)
    return sort_busstop(data=datas, _sort=sort, time_format=time_format)


@app.get("/bus_stop/{city}/clean")
async def bus_stop_clean(*, city: str = Path(..., title="city for get data"), time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    _time: int = int(tm()) - time
    datas = await get_valid_city(city, 'clean', _time, writers)
    return sort_busstop(data=datas, _sort=sort, time_format=time_format)


@app.get("/bus_stop/{city}/dirty/{bus_number}")
async def bus_stop_dirty_bus(city: str, bus_number: str, time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    return await transport_utils.create_bus_info(sort, time_format, bus_number, time, city, 'dirty')


@app.get("/bus_stop/{city}/clean/{bus_number}")
async def bus_stop_clean_bus(city: str, bus_number: str, time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    return await transport_utils.create_bus_info(sort, time_format, bus_number, time, city, 'clean')


@app.get("/trolleybuses_stop/{city}/dirty/{bus_number}")
async def bus_stop_dirty_trolleybuses(city: str, bus_number: str, time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    return await transport_utils.create_trolleybus_info(sort, time_format, bus_number, time, city, 'dirty')


@app.get("/trolleybuses_stop/{city}/clean/{bus_number}")
async def bus_stop_clean_trolleybuses(city: str, bus_number: str, time: int = 3600, sort: str = 'Время', time_format: str = '%H:%M') -> dict:
    return await transport_utils.create_trolleybus_info(sort, time_format, bus_number, time, city, 'clean')
