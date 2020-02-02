from utils.get import get_post_wall, get_comment_data
from utils.validation import cleaning_post, validation_bus_stop, cleaning_post_otherwise
from config import update_time
from asyncio import sleep
from utils.utils import get_max_value_bd
from config import id_groups
import re

class Writer:
    def __init__(self, vk):
        self.vk = vk

    async def write_in_database(self, model):
        name_class = model.__name__.lower()
        data_utils = DataGetter(name_class)
        while True:
            vk_post = data_utils.get_rewrite_post(self.vk)
            data_post = data_utils.get_cleaning_post(vk_post)
            stop = data_utils.get_bus_stop()
            data = validation_bus_stop(data_post, stop)
            datas = list(sorted(data, key=lambda x: x[1]))
            await self.write_data_bd(model, datas, 'time')
            await sleep(update_time)

    @staticmethod
    async def write_data_bd(model, data: list, column_name: str) -> None:
        max_time_bd = await get_max_value_bd(model, column_name)
        for _data in data:
            if _data[1] > max_time_bd:
                await model.objects.create(bus_stop=_data[0], time=_data[1])

class DataGetter:
    def __init__(self, name_class: str):
        self.name_class = name_class

    def get_rewrite_post(self, vk):
        id_group = self.__get_id_group()
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

    def get_cleaning_post(self, vk_post) -> tuple:
        if self.name_class.find('dirty') != -1:
            return cleaning_post(vk_post)
        else:
            return cleaning_post_otherwise(vk_post)
