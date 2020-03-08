from starlette.requests import Request
from fastapi import Depends
from utils.security import get_password_hash, get_current_user, verify_password
from starlette.responses import RedirectResponse
from models.Repositories import UserRepository
from configuration.config import templates


async def logout_and_remove_cookie(request: Request):
    response = RedirectResponse(url=request.url_for('profile'))
    response.delete_cookie("Authorization")
    return response


async def valid_email(request: Request):
    id = request.query_params.get('id')
    if id:
        user = await UserRepository().get_user_id(int(id))
        if not user['is_activatet']:
            await user.update(is_activatet=True)
            return RedirectResponse(url=request.url_for('profile'))
        return RedirectResponse(url="/poshol_na_hoy")


async def show_refresh_password(request: Request):
    return templates.TemplateResponse("user/refresh_password.html", {"request": request})


async def refresh_password(request: Request, user=Depends(get_current_user)):
    form_data = await request.form()
    old_password = form_data.get('password_old')
    new_password = form_data.get('password_new')
    if verify_password(old_password, user.hashed_password):
        new_password_hash = get_password_hash(new_password)
        await user.update(hashed_password=new_password_hash)
        return RedirectResponse(url="/docs", status_code=303)
    return RedirectResponse(url=request.url_for('refresh_password_get'), status_code=303)


async def profile(request: Request, user=Depends(get_current_user)):
    pk = user.user_info.pk
    user_create_at = (await UserRepository().get_two_model(pk)).create_at
    return templates.TemplateResponse("user/profile.html", {"request": request, "user": user, "user_create_at": str(user_create_at)[:19]})
