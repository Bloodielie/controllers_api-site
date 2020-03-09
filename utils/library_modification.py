from fastapi import APIRouter


def route(prefix: str, endpoint, **kwargs):
    return prefix, endpoint, kwargs


class Router(APIRouter):
    def __init__(self, _routers: list, include_in_schema: bool = False):
        super().__init__()
        self.include_in_schema = include_in_schema
        self._routers = _routers
        self.include_routers()

    def include_routers(self) -> None:
        for router in self._routers:
            if self.include_in_schema:
                self.add_api_route(path=router[0], endpoint=router[1], **router[2])
            self.add_api_route(path=router[0], include_in_schema=False, endpoint=router[1], **router[2])
