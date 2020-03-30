from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.datastructures import FormData
from fastapi import Depends

from app.configuration.config_variables import list_bus_stop, writers

from app.utils.utils import get_data_about_transport, get_transport_number_city
from .dependency import verify_city

from app.configuration.config import templates
from typing import Union


async def show_city_choice(request: Request) -> templates.TemplateResponse:
    cities: list = [city for city in list_bus_stop.keys()]
    return templates.TemplateResponse("transport/main.html", {"request": request, 'cities': cities})


async def city_choice(request: Request) -> Union[templates.TemplateResponse, RedirectResponse]:
    form_data: FormData = await request.form()
    city: str = form_data.get('city')
    selected_transport: str = form_data.get('transport_type')
    response = RedirectResponse(f'{city}?selected_transport={selected_transport}', status_code=303)
    return response


async def show_transport_parameters_choice(request: Request, verify=Depends(verify_city)) -> \
        Union[templates.TemplateResponse, RedirectResponse]:
    if verify:
        city = request.path_params.get('city')
        selected_transport = request.query_params.get('selected_transport')
        selected_transport: str = selected_transport if selected_transport in ['bus', 'trolleybus'] else 'bus'
        transport_stop = get_transport_number_city(city, selected_transport)
        return templates.TemplateResponse("transport/transport_parameters_choice.html", {"request": request, "bus_stops": transport_stop})
    return RedirectResponse(url=request.url_for('city_choice'), status_code=303)


async def transport_parameters_choice(request: Request, verify=Depends(verify_city)) -> RedirectResponse:
    if verify:
        city = request.path_params['city']
        selected_transport: str = request.query_params.get('selected_transport')
        selected_transport: str = selected_transport if selected_transport in ['bus', 'trolleybus'] else 'bus'

        form_data: FormData = await request.form()
        transport_number: str = form_data.get('transport_number')
        transport_number = transport_number if transport_number in get_transport_number_city(city, selected_transport) else '12A'

        time: str = form_data.get('text')
        time: int = int(time) if time.isdigit() and int(time) in list(range(100002)) else 10000

        selection_bus_stop = form_data.get('dirty_or_clear')
        selection_bus_stop: str = selection_bus_stop if selection_bus_stop in ['dirty', 'clean'] else 'dirty'

        sort = form_data.get('sort')
        sort: str = sort if sort.lower() in ['сообщения', 'время'] else 'Время'

        data: dict = await get_data_about_transport(time, city, selection_bus_stop, transport_number, writers, sort, selected_transport,
                                                    '%H:%M')

        return templates.TemplateResponse("transport/transport_table.html", {"request": request, 'data': data,
                                                                             'transport_number': transport_number})
    return RedirectResponse(url=request.url_for('city_choice'), status_code=303)


async def show_city_choice_all(request: Request):
    cities: list = [city for city in list_bus_stop.keys()]
    return templates.TemplateResponse("transport/main_all.html", {"request": request, 'cities': cities})


async def city_choice_all(request: Request):
    cities: list = [city for city in list_bus_stop.keys()]
    form_data: FormData = await request.form()
    city = form_data.get('city')
    city = city if city in cities else 'brest'

    selection_bus_stop = form_data.get('dirty_or_clear')
    selection_bus_stop: str = selection_bus_stop if selection_bus_stop in ['dirty', 'clean'] else 'dirty'
    table_name = f'bus_stop_dirty_{city}'
    model = writers.get(city)[0]
    if selection_bus_stop == 'clean':
        model = writers.get(city)[1]
        table_name = table_name.replace('dirty', 'clean')
    query = "SELECT bus_stop as stop, COUNT(bus_stop) as value_msg, to_char(to_timestamp(max(time)), 'HH24:MI DD-MM-YY') as max_time\n" \
            f"FROM {table_name}\n" \
            "GROUP BY bus_stop\n" \
            "ORDER BY value_msg desc;"
    datas = await model.__database__.fetch_all(query=query)
    return templates.TemplateResponse("transport/all_table.html", {"request": request, 'datas': datas, 'city': city})
