import aiohttp
import asyncio
from typing import Union, Dict
from abc import ABC, abstractmethod


class VkApiAbstract(ABC):
    @abstractmethod
    def method(self, method: str, **kwargs):
        raise NotImplementedError


class VkApi(VkApiAbstract):
    def __init__(self, token: str, api_version: str = '5.92', session: aiohttp.ClientSession = None,
                 loop: Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop] = None):
        self._default_params = {'access_token': token, 'v': api_version}
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        self._loop = loop

        if session is None:
            session = aiohttp.ClientSession(loop=self._loop)
        self._session = session

    @property
    def get_default_params(self):
        return self._default_params

    @get_default_params.setter
    def get_default_params(self, value: Dict[str, str]):
        if not value.get('access_token') and not value.get('v'):
            raise TypeError('In default parameters there should be a token and version')
        self._default_params = value

    async def method(self, method: str, **kwargs) -> dict:
        params = self._default_params.copy()
        if kwargs:
            params.update(kwargs)

        async with self._session.get(f'https://api.vk.com/method/{method}', params=params) as response:
            response = await response.json()
            if response.get('error'):
                error = response.get('error')
                raise Exception(f'Vk api error: {error}')
            return response.get('response')
