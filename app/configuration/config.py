import sqlalchemy
from databases import Database
from starlette.config import Config
from starlette.templating import Jinja2Templates

from app.utils.json import get_json

config = Config(".env")

# Main application
VERSION = "0.1.5"
TITLE = 'AntiContollerApi'
DESCRIPTION = "I give you information about controllers in the cities of Belarus"
OPENAPI_URL = "/api/openapi.json"

# JWT
SECRET_KEY = config('SECRET_KEY', cast=str)
ALGORITHM = config('ALGORITHM', cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# VK
TOKEN_VK: str = config('token', cast=str)

# EMAIL
LOGIN_EMAIL: str = config('login_email', cast=str)
PASSWORD_EMAIL: str = config('password_email', cast=str)

# DATABASE
URL_BD: str = config('url_bd', cast=str)
database = Database(URL_BD, min_size=1, max_size=5)
metadata = sqlalchemy.MetaData()
tb_name_brest_dirty: str = "bus_stop_dirty_brest"
tb_name_brest_clean: str = "bus_stop_clean_brest"
tb_name_gomel_dirty: str = "bus_stop_dirty_gomel"
tb_name_gomel_clean: str = "bus_stop_clean_gomel"
tb_name_grodno_dirty: str = "bus_stop_dirty_grodno"
tb_name_grodno_clean: str = "bus_stop_clean_grodno"

# TEMPLATES
templates = Jinja2Templates(directory="app/templates")

# JSON
path_to_json = 'configuration/json'
stop_bus_brest: list = get_json(f'{path_to_json}/stopbus_brest.json')
stop_bus_gomel: list = get_json(f'{path_to_json}/stopbus_gomel.json')
stop_bus_grodno: list = get_json(f'{path_to_json}/stopbus_grodno.json')

brestbus_stop: dict = get_json(f'{path_to_json}/busstop_brest.json')
gomelbus_stop: dict = get_json(f'{path_to_json}/busstop_gomel.json')
grodnobus_stop: dict = get_json(f'{path_to_json}/busstop_grodno.json')

trolleybusesstop_brest: dict = get_json(f'{path_to_json}/trolleybusesstop_brest.json')
trolleybusesstop_gomel: dict = get_json(f'{path_to_json}/trolleybusesstop_gomel.json')
trolleybusesstop_grodno: dict = get_json(f'{path_to_json}/trolleybusesstop_grodno.json')

# SORTING OPTIONS
clean_dirty_word: list = ['чисто', 'как', 'актуально?', 'cтоят на']
clean_clean_word: list = ['чисто', 'стерильно', 'чистота', 'чистенько']

UPDATE_TIME: int = 100

# SPA STATIC FILES
STATIC_DIRECTORY = "../front"

# Celery
CELERY_BROKER_URL = config('REDIS_URL', cast=str)
CELERY_RESULT_BACKEND = config('REDIS_URL', cast=str)
