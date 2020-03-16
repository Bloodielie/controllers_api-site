from fastapi import Depends
import app.api.views as api
from app.user.urls import auth_router, no_auth_router
from app.main import dependency
from app.transport.urls import transport_router
from app.utils.library_modification import application_route, Router

application_routes = [
    application_route(api.router, prefix='/api', tags=["API"]),
    application_route(transport_router, prefix='/transport'),
    application_route(no_auth_router, prefix='/user', dependencies=[Depends(dependency.redirect_if_authorization)]),
    application_route(auth_router, prefix='/user', dependencies=[Depends(dependency.redirect_if_not_authorization)]),
]

app = Router(application_routes=application_routes)
