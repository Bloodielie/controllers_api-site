import aiohttp


class VkApiException(Exception):
    pass


class VkApi:
    def __init__(self, token: str, api_version: str = '5.92'):
        self.default_params = {'access_token': token, 'v': api_version}

    async def method(self, method, **kwargs) -> dict:
        params = self.default_params.copy()
        if kwargs:
            params.update(kwargs)

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vk.com/method/{method}', params=params) as response:
                response = await response.json()
                if response.get('error'):
                    error = response.get('error')
                    error_code = error.get("error_code")
                    error_msg = error.get("error_msg")
                    raise VkApiException(f'Error_code: {error_code}, error_msg: {error_msg}')
                return response.get('response')
