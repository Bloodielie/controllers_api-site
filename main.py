#uvicorn main:app --reload
from fastapi import FastAPI
import vk_api
from config import login, password
import asyncio
from utils.validation import sort_busstop
from time import time as tm
from database import BusStopClear, BusStopDirty, database
from utils.write_in_bd_data import Writer

vk = vk_api.VkApi(login=login, password=password)
vk.auth()
app = FastAPI()

writer = Writer(vk)


@app.on_event("startup")
async def startup():
    await database.connect()
    asyncio.ensure_future(writer.write_in_database(BusStopDirty, 'dirty'))
    asyncio.ensure_future(writer.write_in_database(BusStopClear, 'clean'))


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/bus_stop/dirty")
async def bus_stop_dirty(time: int = 3600, sort: str = 'Время', time_format='%H:%M'):
    _time = int(tm()) - time
    datas = await BusStopDirty.objects.filter(time__gte=_time).all()
    data = sort_busstop(datas, _sort=sort, time_format=time_format)
    return data


@app.get("/bus_stop/clean")
async def bus_stop_clean(time: int = 3600, sort: str = 'Время', time_format='%H:%M'):
    _time = int(tm()) - time
    datas = await BusStopClear.objects.filter(time__gte=_time).all()
    data = sort_busstop(datas, _sort=sort, time_format=time_format)
    return data
