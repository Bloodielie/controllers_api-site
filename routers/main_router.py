from fastapi import APIRouter, Depends
from .api import api
from routers.user.no_auth_router import no_auth_router
from routers.user.auth_router import auth_router
import routers.dependency as depends
from .transport.transport_router import transport_router

app = APIRouter()

app.include_router(api.router, tags=["API"], prefix='/api')

app.include_router(transport_router, prefix='/transport')

app.include_router(no_auth_router, prefix='/user', dependencies=[Depends(depends.redirect_if_authorization)])
app.include_router(auth_router, prefix='/user', dependencies=[Depends(depends.redirect_if_not_authorization)])
