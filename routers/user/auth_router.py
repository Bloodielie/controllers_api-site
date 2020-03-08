from .auth_controller import logout_and_remove_cookie, valid_email, show_refresh_password, refresh_password, profile
from utils.library_modification import route, Router

routers = [
    route('/logout', logout_and_remove_cookie, methods=['GET'], name='logout'),
    route('/valid', valid_email, methods=['GET']),
    route('/refresh_password', show_refresh_password, methods=['GET'], name='refresh_password'),
    route('/refresh_password', refresh_password, methods=['POST']),
    route('/profile', profile, methods=['GET'], name='profile')
]

auth_router = Router(routers)
