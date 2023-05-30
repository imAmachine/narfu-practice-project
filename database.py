from datetime import date

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class DbConnection:
    def __init__(self, key, username, password, host, db):
        self.key = key
        self.username = username
        self.password = password
        self.host = host
        self.db = db

    def db_init(self, app):
        # Настройка подключения к базе данных PostgreSQL
        app.config[self.key] = f'postgresql://{self.username}:{self.password}@{self.host}/{self.db}'
        db.init_app(app)


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_registration = db.Column(db.Date)

    def __init__(self, surname, name, patronymic, mobile, email, date_registration):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.mobile = mobile
        self.email = email
        self.date_registration = date_registration

    def __repr__(self):
        return f"<UserInfo id={self.id}, surname={self.surname}, name={self.name}, " \
               f"patronymic={self.patronymic}, mobile={self.mobile}, email={self.email}, " \
               f"date_registration={self.date_registration}>"


class UserAuth(db.Model):
    __tablename__ = 'user_auth'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return f"<UserAuth id={self.id}, login={self.login}, password={self.password}>"


class RoomResident(db.Model):
    __tablename__ = 'room_resident'

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __init__(self, room_id, user_id):
        self.room_id = room_id
        self.user_id = user_id

    def __repr__(self):
        return f"<RoomResident room_id={self.room_id}, user_id={self.user_id}>"


class Dormitories(db.Model):
    __tablename__ = 'dormitories'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(255))
    title = db.Column(db.String(255))
    address = db.Column(db.String(255))
    info = db.Column(db.String(255))
    description = db.Column(db.String(255))
    status = db.Column(db.Boolean)

    def __init__(self, photo, title, address, info, description, status):
        self.photo = photo
        self.title = title
        self.address = address
        self.info = info
        self.description = description
        self.status = status

    def __repr__(self):
        return f"<Dormitories id={self.id}, photo={self.photo}, title={self.title}, " \
               f"address={self.address}, info={self.info}, description={self.description}, " \
               f"status={self.status}>"


class DormitoriesRooms(db.Model):
    __tablename__ = 'dormitories_rooms'

    id = db.Column(db.Integer, primary_key=True)
    id_dormitories = db.Column(db.Integer, db.ForeignKey('dormitories.id'))
    photo = db.Column(db.String(255))
    room_number = db.Column(db.String(255))
    description = db.Column(db.String(255))
    status = db.Column(db.Boolean)

    def __init__(self, id_dormitories, photo, room_number, description, status):
        self.id_dormitories = id_dormitories
        self.photo = photo
        self.room_number = room_number
        self.description = description
        self.status = status

    def __repr__(self):
        return f"<DormitoriesRooms id={self.id}, id_dormitories={self.id_dormitories}, " \
               f"photo={self.photo}, room_number={self.room_number}, " \
               f"description={self.description}, status={self.status}>"


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('dormitories_rooms.id'))

    def __init__(self, user_id, room_id):
        self.user_id = user_id
        self.room_id = room_id

    def __repr__(self):
        return f"<Application id={self.id}, user_id={self.user_id}, room_id={self.room_id}>"
