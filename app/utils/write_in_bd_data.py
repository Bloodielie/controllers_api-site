import re
from asyncio import sleep
from typing import Iterator

from orm import Model

from app.configuration.config import UPDATE_TIME
from app.configuration.config_variables import id_groups
from app.utils.getting_stops_data import get_max_value_bd
from app.utils.getting_vk_posts import VkPostGetter, VkPostGetterAbstract
from app.utils.validation import cleaning_post, validation_bus_stop, cleaning_post_otherwise
from app.utils.vk_api import VkApiAbstract


class Writer:
    def __init__(self, vk: VkApiAbstract):
        self.vk = vk

    async def write_in_database(self, model: Model) -> None:
        name_class: str = model.__name__.lower()
        post_getter = VkPostGetter(self.vk)
        data_utils = DataGetter(name_class, post_getter)
        while True:
            vk_post: list = await data_utils.get_rewrite_post()
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
    def __init__(self, name_class: str, vk_post_getter: VkPostGetterAbstract):
        self.name_class = name_class
        self.vk_post_getter = vk_post_getter

    async def get_rewrite_post(self):
        id_group: int = self.__get_id_group()
        if self.name_class.find('gomel') != -1:
            return await self.vk_post_getter.comment_data_getter(id_group)
        else:
            return await self.vk_post_getter.post_data_getter(id_group)

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

    def get_cleaning_post(self, vk_post: list) -> Iterator[tuple]:
        if self.name_class.find('dirty') != -1:
            return cleaning_post(vk_post)
        else:
            return cleaning_post_otherwise(vk_post)
