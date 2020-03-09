import orm
import sqlalchemy
from databases import Database
from configuration.config import url_bd, tb_name_brest_dirty, tb_name_brest_clean, tb_name_gomel_dirty, tb_name_gomel_clean, tb_name_grodno_dirty, tb_name_grodno_clean

database = Database(url_bd)
metadata = sqlalchemy.MetaData()


class UserInfo(orm.Model):
    __tablename__ = 'UserInfo'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True, index=True)
    user_name = orm.String(unique=True, index=True, max_length=100)
    create_at = orm.DateTime()
    add_bus_stop_time = orm.DateTime(allow_null=True)


class User(orm.Model):
    __tablename__ = 'Users'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True, index=True)
    user_name = orm.String(unique=True, index=True, max_length=100)
    email = orm.String(unique=True, max_length=100)
    hashed_password = orm.String(max_length=100)
    is_activatet = orm.Boolean(default=False)
    user_info = orm.ForeignKey(UserInfo)


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


engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)
