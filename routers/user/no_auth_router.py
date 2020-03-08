from .no_auth_controller import show_login, login, show_create_account, create_account
from utils.library_modification import route, Router

routers = [
    route('/login', show_login, methods=['GET'], name='login'),
    route('/login', login, methods=['POST']),
    route('/create_account', show_create_account, methods=['GET'], name='create_account'),
    route('/create_account', create_account, methods=['POST'])
]

no_auth_router = Router(routers)
