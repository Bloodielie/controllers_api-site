from utils.json import get_json

path_to_json = '../fastapi/json'

stop_bus_brest: list = get_json(f'{path_to_json}/stopbus_brest.json')
stop_bus_gomel: list = get_json(f'{path_to_json}/stopbus_gomel.json')
stop_bus_grodno: list = get_json(f'{path_to_json}/stopbus_grodno.json')

brestbus_stop: dict = get_json(f'{path_to_json}/busstop_brest.json')
gomelbus_stop: dict = get_json(f'{path_to_json}/busstop_gomel.json')
grodnobus_stop: dict = get_json(f'{path_to_json}/busstop_grodno.json')

trolleybusesstop_brest: dict = get_json(f'{path_to_json}/trolleybusesstop_brest.json')
trolleybusesstop_gomel: dict = get_json(f'{path_to_json}/trolleybusesstop_gomel.json')
trolleybusesstop_grodno: dict = get_json(f'{path_to_json}/trolleybusesstop_grodno.json')

url_bd: str = 'postgresql://postgres:1234@localhost/bus_stop'
tb_name_brest_dirty: str = "bus_stop_dirty"
tb_name_brest_clean: str = "bus_stop_clear"
tb_name_gomel_dirty: str = "bus_stop_dirty_gomel"
tb_name_gomel_clean: str = "bus_stop_clean_gomel"
tb_name_grodno_dirty: str = "bus_stop_dirty_grodno"
tb_name_grodno_clean: str = "bus_stop_clean_grodno"

login: str = ''
password: str = ''

clean_dirty_word: list = ['чисто', 'как', 'актуально?', 'cтоят на']
clean_clean_word: list = ['чисто', 'стерильно', 'чистота', 'чистенько']

update_time: int = 100
