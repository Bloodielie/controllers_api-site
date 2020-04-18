from starlette.requests import Request
from app.client.security.token import TokenTools

token_tools = TokenTools()


async def check_access_token(request: Request):
    token = request.headers.get("Authorization")
    token_verify = await token_tools.check_token(token)
    token_payload = token_tools.get_token_payload(token)
    if token_verify and token_payload.get("type") == 'refresh_token':
        token_verify = False
    token_user_name = None
    if token_payload:
        token_user_name = token_payload.get("sub")
    return [token_verify, token_user_name]
