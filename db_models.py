from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Length


class User(UserMixin):
    def __init__(self, user_id, login, password, name, surname, patronymic, 
                 email, phone_number, date_of_birth, address, health_info, role):
        self.role = role
        self.health_info = health_info
        self.address = address
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.email = email
        self.patronymic = patronymic
        self.surname = surname
        self.name = name
        self.id = user_id
        self.login = login
        self.password = password

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def to_dict(self):
        return {
            'user_id': self.id,
            'login': self.login,
            'password': self.password,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
            'email': self.email,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth,
            'address': self.address,
            'health_info': self.health_info,
            'role': self.role
        }


# Определение класса формы для регистрации пользователя
class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Логин"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Пароль"})
    name = StringField('Name', validators=[DataRequired()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Фамилия"})
    surname = StringField('Surname', validators=[DataRequired()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Имя"})
    patronymic = StringField('Patronymic', render_kw={"class": "loginForm__wrapper__input", "placeholder": "Отчетство"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Email"})
    phone_number = StringField('Phone Number', validators=[DataRequired()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Номер телефона"})
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Дата рождения"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Адрес"},)
    health_info = StringField('Health Information', render_kw={"class": "loginForm__wrapper__input", "placeholder": "Информация о здоровье"})


# Определение класса формы для регистрации пользователя
class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Логин"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"class": "loginForm__wrapper__input", "placeholder": "Пароль"})


class UserInfoDataLk(FlaskForm):
    name = StringField('name', validators=[DataRequired()], render_kw={"class": "lk__input", "placeholder": "Имя"})
    surname = StringField('surname', validators=[DataRequired()], render_kw={"class": "lk__input", "placeholder": "Фамилия"})
    patronymic = StringField('patronymic', validators=[DataRequired()], render_kw={"class": "lk__input", "placeholder": "Отчество"})
    email = StringField('email', validators=[DataRequired(), Email()], render_kw={"class": "lk__input", "placeholder": "Email"})
    phone_number = StringField('phone_number', validators=[DataRequired(), ], render_kw={"class": "lk__input", "placeholder": "Номер телефона"})
    date_of_birth = DateField('date_of_birth', validators=[DataRequired()], render_kw={"class": "lk__input", "placeholder": "Дата рождения"})
    address = StringField('address', validators=[DataRequired()], render_kw={"class": "lk__input", "placeholder": "Ваш адрес прописки"})
    health_info = StringField('health_info', validators=[], render_kw={"class": "lk__input", "placeholder": "Информация о здоровье"})