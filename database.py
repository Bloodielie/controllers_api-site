import orm
import sqlalchemy
from databases import Database
from config import url_bd, tb_name_1, tb_name_2


database = Database(url_bd)
metadata = sqlalchemy.MetaData()


class BusStopDirty(orm.Model):
    __tablename__ = tb_name_1
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()


class BusStopClear(orm.Model):
    __tablename__ = tb_name_2
    __database__ = database
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
    bus_stop = orm.String(max_length=100)
    time = orm.Integer()


engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)
