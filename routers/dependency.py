from starlette.requests import Request
from utils.exceptions import RequiresLoginException, RequiresSystemException


def redirect_if_authorization(request: Request):
    cookie = request.cookies.get("Authorization")
    if cookie:
        if cookie.split()[0].lower() == 'bearer':
            raise RequiresLoginException


def redirect_if_not_authorization(request: Request):
    cookie = request.cookies.get("Authorization")
    if not cookie:
        raise RequiresSystemException