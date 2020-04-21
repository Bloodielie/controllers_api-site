from typing import Union

from fastapi import BackgroundTasks, APIRouter
from starlette.requests import Request

from app.client import pydantic_models
from app.client.security.auth import authenticate_user, get_password_hash, get_email_verify_postfix, verify_password
from app.client.security.token import create_tokens, TokenTools
from app.client.user_repository import UserRepository
from app.utils.email import Email

router = APIRouter()
user_repository = UserRepository()
token_tools = TokenTools()


@router.post('/auth', response_model=Union[pydantic_models.UserAuthOut, pydantic_models.TokenOut])
async def auth(data: pydantic_models.UserAuthIn):
    user = await user_repository.get_user('user_name', data.login)
    authenticate = authenticate_user(user, data.password)
    if not authenticate:
        return pydantic_models.TokenOut(status=False)
    _tokens: list = create_tokens(data={"sub": data.login})
    security_model = await user_repository.get_other_model('user_security', user)
    await security_model.update(refresh_token=_tokens[1])
    return pydantic_models.UserAuthOut(access_token=_tokens[0], refresh_token=_tokens[1])


@router.post('/check_token', response_model=pydantic_models.TokenOut)
async def check_token(data: pydantic_models.TokenIn):
    token_status = await token_tools.check_token(data.token)
    return pydantic_models.TokenOut(status=token_status)


@router.post('/create_account', response_model=Union[pydantic_models.UserAuthOut, pydantic_models.TokenOut])
async def create_account(request: Request, background_tasks: BackgroundTasks, data: pydantic_models.AccountCreateIn):
    if not Email.email_validation(data.email) or await user_repository.is_user_exists(data.email, data.login):
        return pydantic_models.TokenOut(status=False)

    _tokens: list = create_tokens(data={"sub": data.login})
    password_hash = get_password_hash(data.password)
    user_create = pydantic_models.User(user_name=data.login, hashed_password=password_hash, email=data.email,
                                       refresh_token=_tokens[1])

    await user_repository.create_user(user_create)

    postfix: str = get_email_verify_postfix(data.login)
    url = request.url_for('valid_email') + f'?id={postfix}'
    background_tasks.add_task(Email.send_email, data.email, url)

    return pydantic_models.UserAuthOut(access_token=_tokens[0], refresh_token=_tokens[1])


@router.post('/refresh_token', response_model=Union[pydantic_models.UserAuthOut, pydantic_models.TokenOut])
async def refresh_token(data: pydantic_models.RefreshTokenIn):
    user_security = await user_repository.get_refresh_token_model(data.refresh_token)
    if not user_security:
        return pydantic_models.TokenOut(status=False)
    user_name = token_tools.get_user_name_in_token(data.refresh_token)
    if not user_name:
        return pydantic_models.TokenOut(status=False)
    tokens = create_tokens(data={"sub": user_name})
    await user_security.update(refresh_token=tokens[1])
    return pydantic_models.UserAuthOut(access_token=tokens[0], refresh_token=tokens[1])


@router.post('/refresh_password', response_model=pydantic_models.TokenOut)
async def refresh_password(data: pydantic_models.RefreshPasswordIn):
    user = await user_repository.get_user('user_name', data.login)
    if not user or not verify_password(data.old_password, user.hashed_password):
        return pydantic_models.TokenOut(status=False)
    new_password_hash: str = get_password_hash(data.new_password)
    await user.update(hashed_password=new_password_hash)
    return pydantic_models.TokenOut(status=True)


@router.get('/valid_email', name='valid_email', response_model=pydantic_models.TokenOut)
async def valid_email(id: str):
    email_model = await user_repository.get_email_verify(id)
    if email_model and not email_model.is_activatet:
        await email_model.update(is_activatet=True)
        return pydantic_models.TokenOut(status=True)
    return pydantic_models.TokenOut(status=False)
