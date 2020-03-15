from app.utils.json import get_json
from starlette.config import Config
from starlette.templating import Jinja2Templates
from databases import Database
import sqlalchemy

config = Config(".env")

# Main application
VERSION = "0.1.5"
TITLE = 'AntiContollerApi'
DESCRIPTION = "I give you information about controllers in the cities of Belarus"
OPENAPI_URL = "/api/v1/openapi.json"
REDOC_URL = None

# JWT
SECRET_KEY = config('SECRET_KEY', cast=str)
ALGORITHM = config('ALGORITHM', cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = 7200

# VK
LOGIN_VK: str = config('login_vk', cast=str)
PASSWORD_VK: str = config('password_vk', cast=str)

# EMAIL
LOGIN_EMAIL: str = config('login_email', cast=str)
PASSWORD_EMAIL: str = config('password_email', cast=str)

# DATABASE
URL_BD: str = config('url_bd', cast=str)
database = Database(URL_BD)
metadata = sqlalchemy.MetaData()
tb_name_brest_dirty: str = "bus_stop_dirty"
tb_name_brest_clean: str = "bus_stop_clear"
tb_name_gomel_dirty: str = "bus_stop_dirty_gomel"
tb_name_gomel_clean: str = "bus_stop_clean_gomel"
tb_name_grodno_dirty: str = "bus_stop_dirty_grodno"
tb_name_grodno_clean: str = "bus_stop_clean_grodno"

# TEMPLATES
templates = Jinja2Templates(directory="app/templates")

# JSON
path_to_json = 'app/configuration/json'
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
