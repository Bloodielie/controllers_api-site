from app.main.models import BusStopDirtyBrest, BusStopClearBrest, BusStopDirtyGomel, BusStopClearGomel, BusStopDirtyGrodno, BusStopClearGrodno
from .config import brestbus_stop, trolleybusesstop_brest, gomelbus_stop, trolleybusesstop_gomel, grodnobus_stop, trolleybusesstop_grodno, stop_bus_brest, stop_bus_gomel, \
    stop_bus_grodno

writers: dict = {
    'brest': [BusStopDirtyBrest, BusStopClearBrest],
    'gomel': [BusStopDirtyGomel, BusStopClearGomel],
    'grodno': [BusStopDirtyGrodno, BusStopClearGrodno]
}

list_bus_stop: dict = {'brest': [brestbus_stop, trolleybusesstop_brest],
                       'gomel': [gomelbus_stop, trolleybusesstop_gomel],
                       'grodno': [grodnobus_stop, trolleybusesstop_grodno]}

id_groups: dict = {'brest': [72869598, stop_bus_brest],
                   'gomel': [96717639, stop_bus_gomel],
                   'grodno': [71507595, stop_bus_grodno]}
