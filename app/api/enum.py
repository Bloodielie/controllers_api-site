from enum import Enum


class City(str, Enum):
    brest = "brest"
    gomel = "gomel"
    grodno = "grodno"


class BusStopSelection(str, Enum):
    dirty = "dirty"
    clean = "clean"


class TransportType(str, Enum):
    bus = "bus"
    trolleybus = "trolleybus"


class AllDataParameter(str, Enum):
    transport_numbers = 'transport_numbers'
    city_stops = 'city_stops'
    transport_stops = 'transport_stops'


class CitySituationParameter(str, Enum):
    get_situation = 'get_situation'
    get_situation_in_bus_stop = 'get_situation_in_bus_stop'
