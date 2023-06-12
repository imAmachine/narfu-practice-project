import psycopg2
from flask import Flask, render_template, jsonify, g, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Length
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

import jsonworker
from DBService import DBService
from db_models import User
from models import Application, Dormitory, Room, UserAuth, Userinfo

DATABASE = jsonworker.read_json("connection.json")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hui'  # SECRET_KEY
login_manager = LoginManager(app)


def get_db():
    if 'db' not in g:
        connection = psycopg2.connect(dbname=DATABASE['db'],
                                      user=DATABASE['username'],
                                      password=DATABASE['password'],
                                      host=DATABASE['host'],
                                      port=DATABASE['port'])
        g.db = DBService(connection)
    return g.db


def select_sql(query, obj):
    db_service = get_db()
    try:
        rows = db_service.exec_select(query)
        if rows:
            objects_list = [obj(*row) for row in rows]
            objects_dicts = [obj.to_dict() for obj in objects_list]
            return jsonify(objects_dicts)
        else:
            return jsonify({'message': 'Not found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@login_manager.user_loader
def load_user(user_id):
    db_service = get_db()
    query = f"SELECT * FROM userauth WHERE user_id={user_id}"
    user_data = db_service.exec_select(query)[0]
    if user_data:
        user = User(user_data[0], user_data[1], user_data[2])
        return user
    return None


# Закрытие соединения с базой данных после запроса
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.connection.close()


@app.route('/')
def index():
    print(current_user)
    return render_template('index.html', regform=RegistrationForm(), logform=LoginForm())


@app.route('/lk')
@login_required
def profile():
    return render_template('lk.html')


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


@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Маршрут для входа в систему
@app.route('/api/login_user', methods=['POST'])
def auth_user():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        try:
            db_service = get_db()
            query = f"SELECT * FROM userauth WHERE login='{login}' AND password='{password}'"
            user_data = db_service.exec_select(query)[0]
            if user_data:
                user = User(user_data[0], user_data[1], user_data[2])
                login_user(user)
                g.user = user  # Загрузка пользователя в контекст
            else:
                return jsonify({'message': 'Invalid login credentials'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid form data'})


# Регистрация нового пользователя в базе данных
@app.route('/api/registrate_user', methods=['POST'])
def registrate_user():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():
        # Извлечение данных из формы
        login = form.login.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data
        patronymic = form.patronymic.data
        email = form.email.data
        phone_number = form.phone_number.data
        date_of_birth = form.date_of_birth.data.__str__()
        address = form.address.data
        health_info = form.health_info.data
        # Выполнение запроса на регистрацию пользователя
        query = f"CALL registrateuser('{login}','{password}','{name}','{surname}','{patronymic}','{email}','{phone_number}','{date_of_birth}','{address}','{health_info}');"
        try:
            db_service = get_db()
            db_service.exec_procedure(query)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'kakayato huinya'})


# Получение заявки по id пользователя
@app.route('/api/applications/<int:user_id>', methods=['GET'])
def get_application_by_user_id(user_id):
    # Выполнение запроса для получения заявки по id пользователя
    query = f"SELECT * FROM applications WHERE user_id={user_id}"
    return select_sql(query, Application)


# Получение всех общежитий
@app.route('/api/dormitories', methods=['GET'])
def get_all_dormitories():
    # Выполнение запроса для получения всех общежитий
    query = "SELECT * FROM dormitories"
    return select_sql(query, Dormitory)

# Получение всех комнат по id общежития
@app.route('/api/rooms/<int:dormitory_id>', methods=['GET'])
def get_rooms_by_dormitory_id(dormitory_id):
    # Выполнение запроса для получения всех комнат по id общежития
    query = f"SELECT * FROM rooms WHERE dormitory_id={dormitory_id}"
    return select_sql(query, Room)


if __name__ == "__main__":
    app.run(debug=True)
