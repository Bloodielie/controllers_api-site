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
