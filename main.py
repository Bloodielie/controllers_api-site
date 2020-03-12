import asyncio
import vk_api

from configuration.config import login_vk, password_vk, metadata, database
from configuration.config_variables import writers

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from utils.write_in_bd_data import Writer
from models import *

from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from starlette.responses import RedirectResponse
from utils.exceptions import RequiresLoginException, RequiresSystemException

import urls
import sqlalchemy

vk = vk_api.VkApi(login=login_vk, password=password_vk)
vk.auth()

app = FastAPI(
    title="AntiContollerApi",
    description="I give you information about controllers in the cities of Belarus",
    version="0.1.4",
    openapi_url="/api/v1/openapi.json",
    redoc_url=None
    )


@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException):
    return RedirectResponse(url=request.url_for('profile'), status_code=303)


@app.exception_handler(RequiresSystemException)
async def exception_handler(request: Request, exc: RequiresSystemException):
    return RedirectResponse(url=request.url_for('login'), status_code=303)


app.include_router(urls.app)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
    await database.connect()
    for wr in writers:
        data = writers.get(wr)
        for info in data:
            asyncio.create_task(Writer(vk).write_in_database(info))


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
