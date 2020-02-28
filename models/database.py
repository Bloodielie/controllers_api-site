import orm
import sqlalchemy
from databases import Database
from configuration.config import url_bd, tb_name_brest_dirty, tb_name_brest_clean, tb_name_gomel_dirty, tb_name_gomel_clean, tb_name_grodno_dirty, tb_name_grodno_clean

database = Database(url_bd)
metadata = sqlalchemy.MetaData()


class AbstractBusStop(orm.Model):
    __tablename__ = 'test'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()


class BusStopDirty_Brest(AbstractBusStop):
    __tablename__ = tb_name_brest_dirty
    __metadata__ = metadata


class BusStopClear_Brest(AbstractBusStop):
    __tablename__ = tb_name_brest_clean
    __metadata__ = metadata


class BusStopDirty_Grodno(AbstractBusStop):
    __tablename__ = tb_name_grodno_dirty
    __metadata__ = metadata


class BusStopClear_Grodno(AbstractBusStop):
    __tablename__ = tb_name_grodno_clean
    __metadata__ = metadata


class BusStopDirty_Gomel(AbstractBusStop):
    __tablename__ = tb_name_gomel_dirty
    __metadata__ = metadata


class BusStopClear_Gomel(AbstractBusStop):
    __tablename__ = tb_name_gomel_clean
    __metadata__ = metadata


engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)
