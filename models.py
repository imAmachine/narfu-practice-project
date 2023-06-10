import datetime


class UserAuth:
    def __init__(self, user_id, login, password):
        self.user_id = user_id
        self.login = login
        self.password = password

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'password': self.password
        }


class Userinfo:
    def __init__(self, user_id, name, surname, patronymic, email, phone_number, date_of_birth, address, health_info):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.address = address
        self.health_info = health_info

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
            'email': self.email,
            'phone_number': self.phone_number,
            'date_of_birth': str(self.date_of_birth),
            'address': self.address,
            'health_info': self.health_info
        }


class Dormitory:
    def __init__(self, dormitory_id, name, address, photo, description, available_capacity, total_capacity, status):
        self.dormitory_id = dormitory_id
        self.name = name
        self.address = address
        self.photo = photo
        self.description = description
        self.available_capacity = available_capacity
        self.total_capacity = total_capacity
        self.status = status

    def to_dict(self):
        return {
            'dormitory_id': self.dormitory_id,
            'name': self.name,
            'address': self.address,
            'photo': self.photo,
            'description': self.description,
            'available_capacity': self.available_capacity,
            'total_capacity': self.total_capacity,
            'status': self.status
        }


class Application:
    def __init__(self, application_id, user_id, dormitory_id, application_date=datetime.datetime.now(),
                 application_status='In work'):
        self.application_id = application_id
        self.user_id = user_id
        self.dormitory_id = dormitory_id
        self.application_date = application_date
        self.application_status = application_status

    def to_dict(self):
        return {
            'application_id': self.application_id,
            'user_id': self.user_id,
            'dormitory_id': self.dormitory_id,
            'application_date': self.application_date,
            'application_status': self.application_status
        }


class RoomAssignment:
    def __init__(self, assignment_id, user_id, dormitory_id, room_number, check_in_date, check_out_date):
        self.assignment_id = assignment_id
        self.user_id = user_id
        self.dormitory_id = dormitory_id
        self.room_number = room_number
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    def to_dict(self):
        return {
            'assignment_id': self.assignment_id,
            'user_id': self.user_id,
            'dormitory_id': self.dormitory_id,
            'room_number': self.room_number,
            'check_in_date': str(self.check_in_date),
            'check_out_date': str(self.check_out_date)
        }


class Room:
    def __init__(self, room_id, dormitory_id, room_number, status):
        self.room_id = room_id
        self.dormitory_id = dormitory_id
        self.room_number = room_number
        self.status = status

    def to_dict(self):
        return {
            'room_id': self.room_id,
            'dormitory_id': self.dormitory_id,
            'room_number': self.room_number,
            'status': self.status
        }
