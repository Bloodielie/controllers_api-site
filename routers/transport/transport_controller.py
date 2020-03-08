from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.datastructures import FormData

from configuration.config_variables import list_bus_stop, state_transort, writers

from utils.utils import get_data_about_transport, get_transport_number_city

from configuration.config import templates


async def show_city_choice(request: Request):
    cities: list = [city for city in list_bus_stop.keys()]
    return templates.TemplateResponse("transport/main.html", {"request": request, 'cities': cities})


async def city_choice(request: Request):
    form_data: FormData = await request.form()
    city: str = form_data.get('city')
    state_transort['selected_transport'] = form_data.get('transport_type')
    state_transort['city'] = city
    return RedirectResponse(f'{city}', status_code=303)


async def show_transport_parameters_choice(request: Request):
    city = request.path_params['city']
    transport_stop = get_transport_number_city(city, request.state.selected_transport)
    return templates.TemplateResponse("transport/transport_parameters_choice.html", {"request": request, "bus_stops": transport_stop})


async def transport_parameters_choice(request: Request):
    city = request.path_params['city']
    form_data: FormData = await request.form()
    transport_number: str = form_data.get('transport_number')
    state_transort['time'] = form_data.get('text')
    state_transort['selection_bus_stop'] = form_data.get('dirty_or_clear')
    state_transort['transport_number'] = transport_number
    state_transort['city'] = city
    sort = form_data.get('sort')
    if sort:
        state_transort['sort'] = sort
    return RedirectResponse(f'{city}/{transport_number}', status_code=303)


async def transport_view(request: Request):
    city = request.path_params['city']
    transport_number = request.path_params['transport_number']
    time: str = request.state.time
    selection_bus_stop: str = request.state.selection_bus_stop
    sort: str = request.state.sort
    selected_transport: str = request.state.selected_transport
    data: dict = await get_data_about_transport(int(time), city, selection_bus_stop, transport_number, writers, sort, selected_transport, '%H:%M')
    return templates.TemplateResponse("transport/transport_table.html", {"request": request, 'data': data, 'transport_number': transport_number})
