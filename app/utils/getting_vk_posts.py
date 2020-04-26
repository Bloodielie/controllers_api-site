import asyncio
from abc import ABC, abstractmethod
from typing import Union

from app.utils.vk_api import VkApiAbstract


class VkPostGetterAbstract(ABC):
    @abstractmethod
    def post_data_getter(self, group_id: int):
        raise NotImplementedError

    @abstractmethod
    def comment_data_getter(self, group_id: int):
        raise NotImplementedError


class VkPostGetter(VkPostGetterAbstract):
    def __init__(self, vk: VkApiAbstract, post_count: int = 100):
        self._vk = vk
        self.post_count = post_count

    async def post_data_getter(self, group_id: int, post_count: int = None):
        if post_count is None:
            post_count = self.post_count
        wall = await self.get_wall_data(group_id, post_count)
        if wall is None:
            return []

        data = []
        for items in wall:
            data.append((items['text'].lower(), items['date']))
        return data

    async def comment_data_getter(self, group_id: int):
        wall = await self.get_wall_data(group_id, 2)
        if wall is None:
            return []

        comments = await self.comment_getter(wall[0], group_id)
        if len(comments) == 0:
            return []
        await asyncio.sleep(1)
        comments2 = await self.comment_getter(wall[1], group_id)
        if len(comments2) > 0:
            comments.extend(comments2)

        data = []
        for comment in comments:
            try:
                data.append((comment['text'].lower(), comment['date']))
            except KeyError:
                continue
        return data

    async def get_wall_data(self, group_id: int, count: int = 100) -> Union[dict, None]:
        return (await self._vk.method('wall.get', owner_id=-group_id, count=count)).get('items')

    async def comment_getter(self, wall_data: dict, group_id: int) -> Union[list, None]:
        try:
            post_id: int = wall_data['id']
            comment_count: int = wall_data['comments']['count']
            comment_offset = 0 if comment_count < self.post_count else comment_count - self.post_count
            return (await self._vk.method('wall.getComments', owner_id=-group_id, post_id=post_id, count=self.post_count,
                                          offset=comment_offset)).get('items')
        except KeyError:
            return None
