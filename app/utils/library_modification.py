from typing import Callable, Any, List, Union, Optional, Dict, Type

from fastapi import APIRouter
from fastapi.encoders import DictIntStrAny, SetIntStr
from pydantic import BaseModel
from starlette.responses import Response


class ApplicationRoute(BaseModel):
    router: Any
    prefix: str = ""
    tags: List[str] = None
    dependencies: Any = None
    responses: Dict[Union[int, str], Dict[str, Any]] = None
    default_response_class: Optional[Type[Response]] = None


class Route(BaseModel):
    path: str
    endpoint: Callable
    response_model: Type[Any] = None
    status_code: int = 200
    tags: List[str] = None
    dependencies: Any = None
    summary: str = None
    description: str = None
    response_description: str = "Successful Response"
    responses: Dict[Union[int, str], Dict[str, Any]] = None
    deprecated: bool = None
    methods: Optional[Union[set, List[str]]] = None
    operation_id: str = None
    response_model_include: Union[SetIntStr, DictIntStrAny] = None
    response_model_exclude: Union[SetIntStr, DictIntStrAny] = set()
    response_model_by_alias: bool = True
    response_model_skip_defaults: bool = None
    response_model_exclude_unset: bool = False
    include_in_schema: bool = True
    response_class: Type[Response] = None
    name: str = None
    route_class_override: Optional[Type[Any]] = None
    callbacks: List[Any] = None


class Router(APIRouter):
    def __init__(self, routers: List[Union[ApplicationRoute, Route]], include_in_schema: bool = False):
        super().__init__()
        assert isinstance(routers, list), "You must pass a list of routes"
        assert len(routers) > 0, "The list should contain routes"
        self.routers = routers
        self.include_in_schema = include_in_schema
        self.add_routes(self.routers)

    def add_routes(self, routers) -> None:
        for router in routers:
            if isinstance(router, ApplicationRoute):
                self.include_router(**router.dict())
            elif isinstance(router, Route):
                if self.include_in_schema:
                    self.add_api_route(**router.dict())
                    continue
                router.include_in_schema = self.include_in_schema
                self.add_api_route(**router.dict())
            else:
                raise TypeError('You passed the wrong route')
