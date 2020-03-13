from . import views
from app.utils.library_modification import route, Router

routers = [
    route('/', views.show_city_choice, methods=['GET'], name='city_choice'),
    route('/', views.city_choice, methods=['POST']),
    route('/{city}', views.show_transport_parameters_choice, methods=['GET'], name='transport_parameters_choice'),
    route('/{city}', views.transport_parameters_choice, methods=['POST']),
    route('/{city}/{transport_number}', views.transport_view, methods=['GET'], name='transport_view')
]

transport_router = Router(routers)
