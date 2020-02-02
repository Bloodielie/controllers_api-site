from sqlalchemy import desc


async def get_max_value_bd(model, value):
    selection = model.objects.build_select_expression().order_by(desc(value))
    max_value_bd = await model.__database__.execute(selection)
    response = await model.objects.get(id=max_value_bd)
    return response[value]
