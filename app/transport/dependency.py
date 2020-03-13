from starlette.requests import Request
from app.configuration.config_variables import list_bus_stop


def verify_city(request: Request) -> bool:
    city = request.path_params.get('city')
    cities: list = [city for city in list_bus_stop.keys()]
    if city in cities:
        return True
    return False
