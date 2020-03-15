from app.main import models
from . import config

writers: dict = {
    'brest': [models.BusStopDirtyBrest, models.BusStopClearBrest],
    'gomel': [models.BusStopDirtyGomel, models.BusStopClearGomel],
    'grodno': [models.BusStopDirtyGrodno, models.BusStopClearGrodno]
}

list_bus_stop: dict = {'brest': [config.brestbus_stop, config.trolleybusesstop_brest],
                       'gomel': [config.gomelbus_stop, config.trolleybusesstop_gomel],
                       'grodno': [config.grodnobus_stop, config.trolleybusesstop_grodno]}

id_groups: dict = {'brest': [72869598, config.stop_bus_brest],
                   'gomel': [96717639, config.stop_bus_gomel],
                   'grodno': [71507595, config.stop_bus_grodno]}
