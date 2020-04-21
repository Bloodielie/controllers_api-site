from datetime import datetime
from time import time
from typing import Union

from fastapi import Depends, APIRouter

from app.client import pydantic_models
from app.client.user.dependency import check_access_token
from app.client.user_repository import UserRepository
from app.configuration.config_variables import writers
from app.utils.utils import get_stop_city

router = APIRouter()
user_repository = UserRepository()


@router.post('/add_bus_stop', response_model=pydantic_models.TokenOut)
async def add_bus_stop(data: pydantic_models.AddBusStop, token_check: check_access_token = Depends()):
    """Adding a transport stop"""
    if not token_check[0]:
        return pydantic_models.TokenOut(status=False)

    default_type_bus_stop = ['dirty', 'clean']
    cities = writers.keys()
    city = data.city if data.city in cities else None
    if not city:
        return pydantic_models.TokenOut(status=False)
    bus_stops = get_stop_city(city)

    bus_stop = data.bus_stop_name if data.bus_stop_name in bus_stops else None
    type_bus_stop = data.type_bus_stop if data.type_bus_stop in default_type_bus_stop else default_type_bus_stop[0]
    list_key: int = 0 if type_bus_stop == default_type_bus_stop[0] else 1

    user = await user_repository.get_user('user_name', token_check[1])
    email_model = await user_repository.get_other_model('user_email', user)
    if bus_stop and email_model.is_activatet:
        user_two_model = await user_repository.get_other_model('user_info', user)
        if not user_two_model or user_two_model.add_bus_stop_time and user_two_model.add_bus_stop_time.timestamp() >= int(time()) - 900:
            return pydantic_models.TokenOut(status=False)
        model = writers.get(city)[list_key]
        await model.objects.create(bus_stop=bus_stop.lower(), time=int(time()))
        await user_two_model.update(add_bus_stop_time=datetime.now())
        return pydantic_models.TokenOut(status=True)
    return pydantic_models.TokenOut(status=False)


@router.get('/profile', response_model=Union[pydantic_models.TokenOut, pydantic_models.Profile])
async def profile(token_check: check_access_token = Depends()):
    """
    Gives profile information \n
    Still need to pass to header access_token example \n
    HEADER: Authorization: "access_token"
    """
    if not token_check[0]:
        return pydantic_models.TokenOut(status=False)

    user = await user_repository.get_user('user_name', token_check[1])
    user_email = await user_repository.get_other_model('user_email', user)
    user_info = await user_repository.get_other_model('user_info', user)
    data = {
        'user_name': user_info.user_name,
        'create_at': user_info.create_at,
        'add_bus_stop_time': user_info.add_bus_stop_time,
        'email_activatet': user_email.is_activatet,
        'email': user.email
    }
    return data
