import orm
import sqlalchemy
from databases import Database
from config import url_bd, tb_name_brest_dirty, tb_name_brest_clean, tb_name_gomel_dirty, tb_name_gomel_clean, tb_name_grodno_dirty, tb_name_grodno_clean


database = Database(url_bd)
metadata = sqlalchemy.MetaData()


class BusStopDirty_Brest(orm.Model):
    __tablename__ = tb_name_brest_dirty
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()

class BusStopClear_Brest(orm.Model):
    __tablename__ = tb_name_brest_clean
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()


class BusStopDirty_Grodno(orm.Model):
    __tablename__ = tb_name_grodno_dirty
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()

class BusStopClear_Grodno(orm.Model):
    __tablename__ = tb_name_grodno_clean
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()


class BusStopDirty_Gomel(orm.Model):
    __tablename__ = tb_name_gomel_dirty
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()

class BusStopClear_Gomel(orm.Model):
    __tablename__ = tb_name_gomel_clean
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()


engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)
