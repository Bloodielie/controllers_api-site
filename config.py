from utils.json import JsonUtils

stop_bus_brest = JsonUtils('json/stopbus_brest.json').get_json()
stop_bus_gomel = JsonUtils('json/stopbus_gomel.json').get_json()
stop_bus_grodno = JsonUtils('json/stopbus_grodno.json').get_json()

brestbus_stop = JsonUtils('json/busstop_brest.json').get_json()
gomelbus_stop = JsonUtils('json/busstop_gomel.json').get_json()
grodnobus_stop = JsonUtils('json/busstop_grodno.json').get_json()

trolleybusesstop_brest = JsonUtils('json/trolleybusesstop_brest.json').get_json()
trolleybusesstop_gomel = JsonUtils('json/trolleybusesstop_gomel.json').get_json()
trolleybusesstop_grodno = JsonUtils('json/trolleybusesstop_grodno.json').get_json()

url_bd = 'postgresql://postgres:{}@{}}/{}'
tb_name_brest_dirty = "bus_stop_dirty"
tb_name_brest_clean = "bus_stop_clear"
tb_name_gomel_dirty = "bus_stop_dirty_gomel"
tb_name_gomel_clean = "bus_stop_clean_gomel"
tb_name_grodno_dirty = "bus_stop_dirty_grodno"
tb_name_grodno_clean = "bus_stop_clean_grodno"

login = ''
password = ''

list_bus_stop = {'brest': [brestbus_stop, trolleybusesstop_brest],
                 'gomel': [gomelbus_stop, trolleybusesstop_gomel],
                 'grodno': [grodnobus_stop, trolleybusesstop_grodno]}

id_groups = {'brest': [72869598, stop_bus_brest],
             'gomel': [96717639, stop_bus_gomel],
             'grodno': [71507595, stop_bus_grodno]}

clean_dirty_word = ['чисто', 'как', 'актуально?', 'cтоят на']
clean_clean_word = ['чисто', 'стерильно', 'чистота', 'чистенько']

update_time = 100
