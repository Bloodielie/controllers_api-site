from . import views
from app.utils.library_modification import route, Router

routers = [
    route('/all', views.show_city_choice_all, methods=['GET'], name='all_stop'),
    route('/all', views.city_choice_all, methods=['POST']),
    route('/{city}', views.show_transport_parameters_choice, methods=['GET'], name='transport_parameters_choice'),
    route('/{city}', views.transport_parameters_choice, methods=['POST']),
    route('/', views.show_city_choice, methods=['GET'], name='city_choice'),
    route('/', views.city_choice, methods=['POST']),
]

transport_router = Router(routers)
