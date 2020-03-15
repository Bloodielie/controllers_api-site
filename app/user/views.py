from fastapi import Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder

from app.utils.security import get_current_user, verify_password, authenticate_user, create_access_token, get_password_hash, add_cookie
from app.utils.email import Email

from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.configuration.config import ACCESS_TOKEN_EXPIRE_MINUTES, templates

from .pydantic_models import User
from .user_repository import UserRepository

from typing import Union
from starlette.datastructures import FormData


async def logout_and_remove_cookie(request: Request) -> RedirectResponse:
    response = RedirectResponse(url=request.url_for('profile'))
    response.delete_cookie("Authorization")
    return response


async def valid_email(request: Request, user_in_token=Depends(get_current_user)) -> RedirectResponse:
    id: str = request.query_params.get('id')
    if id.isdigit():
        user_in_url = await UserRepository.get_user_id(int(id))
        if user_in_url['id'] == user_in_token['id'] and not user_in_url['is_activatet']:
            await user_in_url.update(is_activatet=True)
            return RedirectResponse(url=request.url_for('profile'))
        return RedirectResponse(url=request.url_for('logout'))
    return RedirectResponse(url=request.url_for('login'))


async def show_refresh_password(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("user/refresh_password.html", {"request": request})


async def refresh_password(request: Request, user=Depends(get_current_user)) -> RedirectResponse:
    form_data: FormData = await request.form()
    old_password: str = form_data.get('password_old')
    new_password: str = form_data.get('password_new')
    if verify_password(old_password, user.hashed_password):
        new_password_hash: str = get_password_hash(new_password)
        await user.update(hashed_password=new_password_hash)
        return RedirectResponse(url="/docs", status_code=303)
    return RedirectResponse(url=request.url_for('refresh_password_get'), status_code=303)


async def profile(request: Request, user=Depends(get_current_user)) -> Union[templates.TemplateResponse, RedirectResponse]:
    if not user:
        return RedirectResponse(request.url_for('logout'), status_code=303)
    pk: int = user.user_info.pk
    user_create_at = (await UserRepository.get_two_model(pk)).create_at
    return templates.TemplateResponse("user/profile.html", {"request": request, "user": user, "user_create_at": str(user_create_at)[:19]})


async def show_login(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("user/login.html", {"request": request})


async def login(request: Request) -> Union[templates.TemplateResponse, RedirectResponse]:
    form_data: FormData = await request.form()
    username: str = form_data.get('login')
    password: str = form_data.get('password')
    user = await UserRepository.get_user_by_name(username)
    authenticate = authenticate_user(user, password)
    if not authenticate:
        return templates.TemplateResponse("user/login.html", {"request": request, 'not_auth': True})

    access_token: bytes = create_access_token(data={"sub": username}, minute=ACCESS_TOKEN_EXPIRE_MINUTES)
    token: str = jsonable_encoder(access_token)

    response = RedirectResponse(url=request.url_for('profile'), status_code=303)
    max_age: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    add_cookie(response, token, max_age)
    return response


async def show_create_account(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("user/create_account.html", {"request": request})


async def create_account(request: Request, background_tasks: BackgroundTasks) -> Union[templates.TemplateResponse, RedirectResponse]:
    form_data: FormData = await request.form()
    username: str = form_data.get('login')
    password: str = form_data.get('password')
    email: str = form_data.get('email')
    if not Email.email_validation(email):
        return templates.TemplateResponse("user/create_account.html", {"request": request, 'not_valid_email': True})
    if await UserRepository.is_user_exists(email, username):
        return templates.TemplateResponse("user/create_account.html", {"request": request, 'user_exists': True})
    password_hash = get_password_hash(password)
    user_create = User(user_name=username, hashed_password=password_hash, email=email)
    await UserRepository.create_user(user_create)

    id = (await UserRepository.get_user_by_name(username))['id']
    url = request.url_for('valid_email') + f'?id={id}'
    background_tasks.add_task(Email.send_email, email, url)

    access_token: bytes = create_access_token(data={"sub": username}, minute=ACCESS_TOKEN_EXPIRE_MINUTES)
    token: str = jsonable_encoder(access_token)

    response = RedirectResponse(url="/docs", status_code=303)
    max_age: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    add_cookie(response, token, max_age)
    return response
