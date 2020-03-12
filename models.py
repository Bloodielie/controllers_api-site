import orm
from configuration.config import tb_name_brest_dirty, tb_name_brest_clean, tb_name_gomel_dirty, tb_name_gomel_clean, tb_name_grodno_dirty, tb_name_grodno_clean, database, metadata


class AbstractBusStop(orm.Model):
    __tablename__ = 'test'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()


class BusStopDirtyBrest(AbstractBusStop):
    __tablename__ = tb_name_brest_dirty
    __metadata__ = metadata


class BusStopClearBrest(AbstractBusStop):
    __tablename__ = tb_name_brest_clean
    __metadata__ = metadata


class BusStopDirtyGrodno(AbstractBusStop):
    __tablename__ = tb_name_grodno_dirty
    __metadata__ = metadata


class BusStopClearGrodno(AbstractBusStop):
    __tablename__ = tb_name_grodno_clean
    __metadata__ = metadata


class BusStopDirtyGomel(AbstractBusStop):
    __tablename__ = tb_name_gomel_dirty
    __metadata__ = metadata


class BusStopClearGomel(AbstractBusStop):
    __tablename__ = tb_name_gomel_clean
    __metadata__ = metadata
