from app.utils.get import get_post_wall, get_comment_data
from app.utils.validation import cleaning_post, validation_bus_stop, cleaning_post_otherwise
from app.configuration.config import UPDATE_TIME
from asyncio import sleep
from app.utils.db import get_max_value_bd
from app.configuration.config_variables import id_groups
import re
from vk_api import VkApi
from orm import Model
from typing import Tuple


class Writer:
    def __init__(self, vk: VkApi):
        self.vk = vk

    async def write_in_database(self, model: Model) -> None:
        name_class: str = model.__name__.lower()
        data_utils = DataGetter(name_class)
        while True:
            vk_post: tuple = data_utils.get_rewrite_post(self.vk)
            data_post = data_utils.get_cleaning_post(vk_post)
            stop: list = data_utils.get_bus_stop()
            data: list = validation_bus_stop(data_post, stop)
            datas: list = list(sorted(data, key=lambda x: x[1]))
            await self.write_data_bd(model, datas, 'time')
            await sleep(UPDATE_TIME)

    @staticmethod
    async def write_data_bd(model: Model, data: list, column_name: str) -> None:
        max_time_bd: int = await get_max_value_bd(model, column_name)
        for _data in data:
            if _data[1] > max_time_bd:
                await model.objects.create(bus_stop=_data[0], time=_data[1])


class DataGetter:
    def __init__(self, name_class: str):
        self.name_class = name_class

    def get_rewrite_post(self, vk: VkApi) -> Tuple[str, int]:
        id_group: int = self.__get_id_group()
        if self.name_class.find('gomel') != -1:
            return get_comment_data(vk, id_group)
        else:
            return get_post_wall(vk, id_group)

    def get_bus_stop(self) -> list:
        for key_city in id_groups.keys():
            city_name = re.search(key_city, self.name_class)
            if not city_name:
                continue
            else:
                return id_groups.get(city_name[0])[1]

    def __get_id_group(self) -> int:
        for key_city in id_groups.keys():
            city_name = re.search(key_city, self.name_class)
            if not city_name:
                continue
            else:
                return id_groups.get(city_name[0])[0]

    def get_cleaning_post(self, vk_post: tuple) -> Tuple[str, int]:
        if self.name_class.find('dirty') != -1:
            return cleaning_post(vk_post)
        else:
            return cleaning_post_otherwise(vk_post)
