from fastapi import APIRouter
from starlette.websockets import WebSocket

from app.client.security.token import TokenTools, create_tokens
from app.client.user_repository import UserRepository

router = APIRouter()
user_repository = UserRepository()
token_tools = TokenTools()


@router.websocket('/check_token')
async def check_token(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        token_status = await token_tools.check_token(data.get('token'))
        await websocket.send_json({'status': token_status})


@router.websocket('/refresh_token')
async def refresh_token(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        refresh_token = data.get('refresh_token')
        if not refresh_token:
            await websocket.send_json({'status': False})
        user_security = await user_repository.get_refresh_token_model(refresh_token)
        if not user_security:
            await websocket.send_json({'status': False})
        user_name = token_tools.get_user_name_in_token(refresh_token)
        if not user_name:
            await websocket.send_json({'status': False})
        tokens = create_tokens(data={"sub": user_name})
        await user_security.update(refresh_token=tokens[1])
        await websocket.send_json({'access_token': tokens[0], 'refresh_token': tokens[1]})
