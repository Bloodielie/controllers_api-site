from .transport_controller import show_city_choice, city_choice, show_transport_parameters_choice, transport_parameters_choice, transport_view
from utils.library_modification import route, Router

routers = [
    route('/', show_city_choice, methods=['GET'], name='city_choice'),
    route('/', city_choice, methods=['POST']),
    route('/{city}', show_transport_parameters_choice, methods=['GET'], name='transport_parameters_choice'),
    route('/{city}', transport_parameters_choice, methods=['POST']),
    route('/{city}/{transport_number}', transport_view, methods=['GET'], name='transport_view')
]

transport_router = Router(routers)
