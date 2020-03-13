from . import views
from app.utils.library_modification import route, Router

auth_routers = [
    route('/logout', views.logout_and_remove_cookie, methods=['GET'], name='logout'),
    route('/valid', views.valid_email, methods=['GET'], name='valid_email'),
    route('/refresh_password', views.show_refresh_password, methods=['GET'], name='refresh_password'),
    route('/refresh_password', views.refresh_password, methods=['POST']),
    route('/profile', views.profile, methods=['GET'], name='profile')
]

no_auth_routers = [
    route('/login', views.show_login, methods=['GET'], name='login'),
    route('/login', views.login, methods=['POST']),
    route('/create_account', views.show_create_account, methods=['GET'], name='create_account'),
    route('/create_account', views.create_account, methods=['POST'])
]

auth_router = Router(auth_routers)
no_auth_router = Router(no_auth_routers)
