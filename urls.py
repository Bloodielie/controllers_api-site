from fastapi import Depends
import api.views as api
from user.urls import auth_router, no_auth_router
import dependency as depends
from transport.urls import transport_router
from utils.library_modification import application_route, Router

routers = [
    application_route(api.router, prefix='/api', tags=["API"]),
    application_route(transport_router, prefix='/transport'),
    application_route(no_auth_router, prefix='/user', dependencies=[Depends(depends.redirect_if_authorization)]),
    application_route(auth_router, prefix='/user', dependencies=[Depends(depends.redirect_if_not_authorization)]),
]

app = Router(application_routes=routers)
