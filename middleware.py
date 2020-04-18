import os
from typing import List

from fastapi.responses import FileResponse
from starlette.datastructures import URL
from starlette.types import ASGIApp, Receive, Scope, Send


class FrontMiddleware:
    def __init__(self, app: ASGIApp, path_to_html: str, static_directory: str, not_static_url: List[str] = None) -> None:
        self.app = app
        self.static_files = os.listdir(static_directory)
        self.path_to_html = path_to_html
        if not_static_url:
            self.static_files.extend(not_static_url)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        url = URL(scope=scope)
        if url.path.split('/')[1] not in self.static_files:
            response = FileResponse(self.path_to_html)
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)
