from orm import models, exceptions
from sqlalchemy import desc


async def get_max_value_bd(model: models, value) -> int:
    """ Getting the maximum value in the database """
    selection = model.objects.build_select_expression().order_by(desc(value))
    max_value_bd = await model.__database__.execute(selection)
    try:
        response = await model.objects.get(id=max_value_bd)
        return response[value]
    except exceptions.NoMatch:
        return 1


async def get_city_data(city: str, type_getter: str, time: int, writers: dict) -> list:
    """ Getting information about the city """
    db_class = writers.get(city.lower())
    if not db_class:
        return [{'bus_stop': 'Wrong city', 'time': 228}]
    elif type_getter == 'dirty':
        return await db_class[0].objects.filter(time__gte=time).all()
    elif type_getter == 'clean':
        return await db_class[1].objects.filter(time__gte=time).all()
