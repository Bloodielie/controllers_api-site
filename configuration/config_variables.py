from models.database import BusStopDirty_Brest, BusStopClear_Brest, BusStopDirty_Gomel, BusStopClear_Gomel, BusStopDirty_Grodno, BusStopClear_Grodno
from .config import brestbus_stop, trolleybusesstop_brest, gomelbus_stop, trolleybusesstop_gomel, grodnobus_stop, trolleybusesstop_grodno, stop_bus_brest, stop_bus_gomel, \
    stop_bus_grodno

writers: dict = {
    'brest': [BusStopDirty_Brest, BusStopClear_Brest],
    'gomel': [BusStopDirty_Gomel, BusStopClear_Gomel],
    'grodno': [BusStopDirty_Grodno, BusStopClear_Grodno]
}

list_bus_stop: dict = {'brest': [brestbus_stop, trolleybusesstop_brest],
                       'gomel': [gomelbus_stop, trolleybusesstop_gomel],
                       'grodno': [grodnobus_stop, trolleybusesstop_grodno]}

id_groups: dict = {'brest': [72869598, stop_bus_brest],
                   'gomel': [96717639, stop_bus_gomel],
                   'grodno': [71507595, stop_bus_grodno]}

state_transort: dict = {
    'city': 'Brest',
    'time': '3600',
    'sort': 'Время',
    'time_format': '%H:%M',
    'selected_transport': 'bus',
    'selection_bus_stop': 'dirty'
}
