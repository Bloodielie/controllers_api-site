import os
from typing import List

from fastapi.responses import FileResponse
from starlette.datastructures import URL
from starlette.types import ASGIApp, Receive, Scope, Send


class FrontMiddleware:
    def __init__(self, app: ASGIApp, static_directory: str, html_name: str = 'index.html', not_static_url: List[str] = None) -> None:
        self.app = app
        self.static_files = os.listdir(static_directory)
        if not self.check_html_in_directory(html_name, self.static_files):
            raise Exception('Html not found in directory')
        self.path_to_html = static_directory + f'/{html_name}'

        if not_static_url:
            data = self.replace_waste_value(not_static_url)
            self.static_files.extend(data)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        print(scope["type"])
        url = URL(scope=scope)
        if url.path.split('/')[1] not in self.static_files:
            response = FileResponse(self.path_to_html)
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)

    @staticmethod
    def replace_waste_value(data: List[str]) -> List[str]:
        _list = []
        for value in data:
            _list.append(value.replace('/', ''))
        return _list

    @staticmethod
    def check_html_in_directory(html_name: str, file_names_in_directory: List[str]) -> bool:
        data = list(filter(lambda x: x == html_name, file_names_in_directory))
        if len(data) == 0:
            return False
        return True
