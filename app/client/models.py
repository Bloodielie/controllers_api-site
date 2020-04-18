import orm

from app.configuration.config import metadata, database


class UserInfo(orm.Model):
    __tablename__ = 'UserInfo'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True)
    user_name = orm.String(unique=True, index=True, max_length=100)
    create_at = orm.DateTime()
    add_bus_stop_time = orm.DateTime(allow_null=True)


class UserSecurity(orm.Model):
    __tablename__ = 'UserSecurity'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True, index=True)
    refresh_token = orm.String(unique=True, max_length=200, index=True)


class UserEmail(orm.Model):
    __tablename__ = 'UserEmail'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True)
    email_verify = orm.String(max_length=70, index=True)
    is_activatet = orm.Boolean(default=False)


class User(orm.Model):
    __tablename__ = 'Users'
    __metadata__ = metadata
    __database__ = database
    id = orm.Integer(primary_key=True, index=True)
    user_name = orm.String(unique=True, index=True, max_length=100)
    email = orm.String(unique=True, max_length=100)
    hashed_password = orm.String(max_length=100)
    user_info = orm.ForeignKey(UserInfo)
    user_security = orm.ForeignKey(UserSecurity)
    user_email = orm.ForeignKey(UserEmail)
