import app.api.views as api
import app.client.auth.views as auth
import app.client.user.views as user

from app.utils.library_modification import application_route, Router

application_routes = [
    application_route(user.router, tags=["USER"], prefix='/user'),
    application_route(auth.router, tags=["AUTH"]),
    application_route(api.router, tags=["API"]),
]

app = Router(application_routes=application_routes)
