import asyncio
import sqlalchemy
from fastapi import FastAPI
from app.main import urls

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from app.configuration import config
from app.configuration.config_variables import writers

from app.utils.write_in_bd_data import Writer
from app.utils.exceptions import RequiresLoginException, RequiresSystemException

from app.utils.vk_api import VkApi
import uvicorn
import os

vk = VkApi(token=config.TOKEN_VK)

app = FastAPI(title=config.TITLE, description=config.DESCRIPTION, version=config.VERSION, openapi_url=config.OPENAPI_URL,
              redoc_url=config.REDOC_URL)

app.include_router(urls.app)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException):
    return RedirectResponse(url=request.url_for('profile'), status_code=303)


@app.exception_handler(RequiresSystemException)
async def exception_handler(request: Request, exc: RequiresSystemException):
    return RedirectResponse(url=request.url_for('login'), status_code=303)


@app.on_event("startup")
async def startup() -> None:
    engine = sqlalchemy.create_engine(str(config.database.url))
    config.metadata.create_all(engine)
    await config.database.connect()
    for wr in writers:
        data = writers.get(wr)
        for info in data:
            await asyncio.sleep(2)
            asyncio.create_task(Writer(vk).write_in_database(info))


@app.on_event("shutdown")
async def shutdown() -> None:
    await config.database.disconnect()

if __name__ == "__main__":
    port = os.environ.get('PORT')
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), log_level="info")
