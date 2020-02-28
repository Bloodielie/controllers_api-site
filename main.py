import asyncio
import vk_api

from configuration.config import login, password
from configuration.config_variables import writers

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from utils.write_in_bd_data import Writer
from models.database import *

from routers import api

vk = vk_api.VkApi(login=login, password=password)
vk.auth()

app = FastAPI(
    title="AntiContollerApi",
    description="I give you information about controllers in the cities of Belarus",
    version="0.1.3",
    openapi_url="/api/v1/openapi.json"
    )

writer = Writer(vk)

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

app.include_router(api.router, prefix='/bus_stop', tags=["api"])
