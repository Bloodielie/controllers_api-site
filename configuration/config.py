from utils.json import get_json
from starlette.config import Config
from starlette.templating import Jinja2Templates
from databases import Database
import sqlalchemy

config = Config(".env")

SECRET_KEY = config('SECRET_KEY', cast=str)
ALGORITHM = config('ALGORITHM', cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = 7200

login_vk: str = config('login_vk', cast=str)
password_vk: str = config('password_vk', cast=str)

login_email: str = config('login_email', cast=str)
password_email: str = config('password_email', cast=str)

url_bd: str = config('url_bd', cast=str)

templates = Jinja2Templates(directory="templates")

path_to_json = 'configuration/json'

database = Database(url_bd)
metadata = sqlalchemy.MetaData()

stop_bus_brest: list = get_json(f'{path_to_json}/stopbus_brest.json')
stop_bus_gomel: list = get_json(f'{path_to_json}/stopbus_gomel.json')
stop_bus_grodno: list = get_json(f'{path_to_json}/stopbus_grodno.json')

brestbus_stop: dict = get_json(f'{path_to_json}/busstop_brest.json')
gomelbus_stop: dict = get_json(f'{path_to_json}/busstop_gomel.json')
grodnobus_stop: dict = get_json(f'{path_to_json}/busstop_grodno.json')

trolleybusesstop_brest: dict = get_json(f'{path_to_json}/trolleybusesstop_brest.json')
trolleybusesstop_gomel: dict = get_json(f'{path_to_json}/trolleybusesstop_gomel.json')
trolleybusesstop_grodno: dict = get_json(f'{path_to_json}/trolleybusesstop_grodno.json')

tb_name_brest_dirty: str = "bus_stop_dirty"
tb_name_brest_clean: str = "bus_stop_clear"
tb_name_gomel_dirty: str = "bus_stop_dirty_gomel"
tb_name_gomel_clean: str = "bus_stop_clean_gomel"
tb_name_grodno_dirty: str = "bus_stop_dirty_grodno"
tb_name_grodno_clean: str = "bus_stop_clean_grodno"

clean_dirty_word: list = ['чисто', 'как', 'актуально?', 'cтоят на']
clean_clean_word: list = ['чисто', 'стерильно', 'чистота', 'чистенько']

update_time: int = 100
