from typing import Callable

from fastapi import APIRouter


def route(prefix: str, endpoint: Callable, **kwargs):
    return prefix, endpoint, kwargs


def application_route(router: Callable, **kwargs):
    return router, kwargs


class Router(APIRouter):
    def __init__(self, api_routers: list = None, application_routes: list = None, include_in_schema: bool = False):
        super().__init__()
        if api_routers:
            self.api_routers = api_routers
            self.include_in_schema = include_in_schema
            self.adding_api_routes()
        if application_routes:
            self.application_routes = application_routes
            self.include_application_routes()

    def adding_api_routes(self) -> None:
        for router in self.api_routers:
            if self.include_in_schema:
                self.add_api_route(path=router[0], endpoint=router[1], **router[2])
            self.add_api_route(path=router[0], include_in_schema=False, endpoint=router[1], **router[2])

    def include_application_routes(self) -> None:
        for router in self.application_routes:
            self.include_router(router=router[0], **router[1])
