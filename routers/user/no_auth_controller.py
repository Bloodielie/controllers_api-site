from starlette.requests import Request
from utils.security import authenticate_user, create_access_token, get_password_hash, add_cookie
from starlette.responses import RedirectResponse
from configuration.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.encoders import jsonable_encoder
from models.models import User
from utils.email import email_validation, send_email
from models.Repositories import UserRepository
from configuration.config import templates


async def show_login(request: Request):
    return templates.TemplateResponse("user/login.html", {"request": request})


async def login(request: Request):
    form_data = await request.form()
    username = form_data.get('login')
    password = form_data.get('password')
    user = await UserRepository().get_user_by_name(username)
    authenticate = authenticate_user(user, password)
    if not authenticate:
        return templates.TemplateResponse("user/login.html", {"request": request, 'not_auth': True})

    access_token = create_access_token(data={"sub": username}, minute=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jsonable_encoder(access_token)

    response = RedirectResponse(url=request.url_for('profile'), status_code=303)
    max_age = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    add_cookie(response, token, max_age)
    return response


async def show_create_account(request: Request):
    return templates.TemplateResponse("user/create_account.html", {"request": request})


async def create_account(request: Request):
    form_data = await request.form()
    username = form_data.get('login')
    password = form_data.get('password')
    email = form_data.get('email')
    if not email_validation(email):
        return templates.TemplateResponse("user/create_account.html", {"request": request, 'not_valid_email': True})
    if await UserRepository().is_user_exists(email, username):
        return templates.TemplateResponse("user/create_account.html", {"request": request, 'user_exists': True})
    password_hash = get_password_hash(password)
    user_create = User(user_name=username, hashed_password=password_hash, email=email)
    await UserRepository().create_user(user_create)
    id = (await UserRepository().get_user_by_name(username))['id']
    origin = request.headers['origin']
    url = f'{origin}/user/valid?id={id}'
    send_email(request.state.server_email, email, url)

    access_token = create_access_token(data={"sub": username}, minute=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jsonable_encoder(access_token)

    response = RedirectResponse(url="/docs", status_code=303)
    max_age = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    add_cookie(response, token, max_age)
    return response
