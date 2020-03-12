from sqlalchemy import desc
from orm import models


async def get_max_value_bd(model: models, value) -> int:
    selection = model.objects.build_select_expression().order_by(desc(value))
    max_value_bd = await model.__database__.execute(selection)
    response = await model.objects.get(id=max_value_bd)
    return response[value]


async def get_city_data(city: str, type_getter: str, _time: int, writers: dict) -> list:
    city = city.lower()
    db_class = writers.get(city)
    if not db_class:
        return [{'bus_stop': 'Wrong city', 'time': 228}]
    elif type_getter == 'dirty':
        return await db_class[0].objects.filter(time__gte=_time).all()
    elif type_getter == 'clean':
        return await db_class[1].objects.filter(time__gte=_time).all()
