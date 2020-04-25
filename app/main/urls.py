import app.api.views as api
import app.client.auth.views as auth
import app.client.user.views as user

from app.utils.library_modification import Router, ApplicationRoute

application_routes = [
    ApplicationRoute(router=user.router, tags=["USER"], prefix='/user'),
    ApplicationRoute(router=auth.router, tags=["AUTH"]),
    ApplicationRoute(router=api.router, tags=["API"]),
]

app = Router(application_routes=application_routes)
