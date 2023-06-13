import psycopg2
from flask import Flask, render_template, jsonify, g, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import jsonworker
from DBService import DBService
from db_models import User, RegistrationForm, LoginForm, UserInfoDataLk
from models import Application, Dormitory, Room, Userinfo

DATABASE = jsonworker.read_json("connection.json")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hui'  # SECRET_KEY
login_manager = LoginManager(app)
login_manager.login_view = 'login'


def connect_db():
    connection = psycopg2.connect(dbname=DATABASE['db'],
                                  user=DATABASE['username'],
                                  password=DATABASE['password'],
                                  host=DATABASE['host'],
                                  port=DATABASE['port'])
    return DBService(connection)


def get_db():
    return connect_db()  # Возвращение соединения с базой данных


def rows_to_dict(rows, obj):
    if rows:
        objects_list = [obj(*row) for row in rows]
        objects_dicts = [obj.to_dict() for obj in objects_list]
        return objects_dicts
    else:
        return None


@login_manager.user_loader
def load_user(user_id):
    db_service = get_db()
    query = f"SELECT userauth.user_id, userauth.login, userauth.\"password\", userinfo.\"name\", " \
            f"userinfo.surname, userinfo.patronymic, userinfo.email, userinfo.phone_number, " \
            f"userinfo.date_of_birth, userinfo.address, userinfo.health_info, userinfo.\"role\" " \
            f"FROM userauth, userinfo WHERE userauth.user_id={user_id} and userinfo.user_id={user_id}"
    user_data = db_service.exec_select(query)
    if user_data:
        row = rows_to_dict(user_data, User)[0]
        user = User(
            user_id=row['user_id'],
            login=row['login'],
            password=row['password'],
            name=row['name'],
            surname=row['surname'],
            patronymic=row['patronymic'],
            email=row['email'],
            phone_number=row['phone_number'],
            date_of_birth=row['date_of_birth'],
            address=row['address'],
            health_info=row['health_info'],
            role=row['role']
        )
        return user
    return None


@app.route('/')
def index():
    return render_template('index.html', regform=RegistrationForm(), logform=LoginForm())


@app.route('/lk')
@login_required
def profile():
    # db_service = get_db()
    # query = ''
    # if current_user.role == 'user':
    #     query = f"SELECT * FROM applications_view WHERE user_id={current_user.id}"
    # elif current_user.role == 'admin':
    #     query = f"SELECT * FROM applications_view"
    # user_data = db_service.exec_select(query)
    return render_template('lk.html', user_form=UserInfoDataLk())


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
            query = f"SELECT user_id FROM userauth WHERE login='{login}' AND password='{password}'"
            user_id = db_service.exec_select(query)
            if user_id:
                user = load_user(user_id[0][0])
                if user:
                    login_user(user)
                    g.user = user  # Загрузка пользователя в контекст

                    # Закрытие курсора
                    db_service.connection.commit()
                    db_service.cursor.close()
            return redirect(url_for('index'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid form data'})


@app.route('/api/add_application/')
@login_required
def add_application():
    dormitory_id = request.args.get('dormitory_id')
    room_id = request.args.get('room_id')
    user_id = request.args.get('user_id')

    query = f"INSERT INTO applications (dormitory_id, room_id, user_id) VALUES ({dormitory_id}, {room_id}, {user_id})"
    try:
        db_service = get_db()
        db_service.exec_query(query)
        return jsonify({'message': 'Application successfully added'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/change_user_data/')
def update_user_data():
    form = UserInfoDataLk(request.form)
    if form.validate_on_submit():
        name = request.args.get('name')
        surname = request.args.get('surname')
        patronymic = request.args.get('patronymic')
        email = request.args.get('email')
        phone_number = request.args.get('phone_number')
        date_of_birth = request.args.get('date_of_birth')
        address = request.args.get('address')
        health_info = request.args.get('health_info')

        query = f"UPDATE userinfo SET name='{name}', " \
                f"surname='{surname}', patronymic='{patronymic}', " \
                f"email='{email}', phone_number='{phone_number}', " \
                f"date_of_birth='{date_of_birth}', address='{address}', " \
                f"health_info='{health_info}' WHERE user_id = {current_user.id}"
        try:
            db_service = get_db()
            db_service.exec_query(query)
            g.user = load_user(current_user.id)
            return redirect(url_for('lk'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Form validation error'}), 500


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
            db_service.exec_query(query)
            return redirect(url_for('index'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'kakayato huinya'})


# Получение заявки по id пользователя
@app.route('/api/applications/<int:user_id>', methods=['GET'])
def get_application_by_user_id(user_id):
    db_service = get_db()
    try:
        # Выполнение запроса для получения заявки по id пользователя
        query = f"SELECT * FROM applications WHERE user_id={user_id}"
        rows = db_service.exec_select(query)
        dict_of_rows = rows_to_dict(rows, Application)
        return jsonify(dict_of_rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Получение всех общежитий
@app.route('/api/dormitories', methods=['GET'])
def get_all_dormitories():
    db_service = get_db()
    try:
        # Выполнение запроса для получения всех общежитий
        query = "SELECT * FROM dormitories"
        rows = db_service.exec_select(query)
        dict_of_rows = rows_to_dict(rows, Dormitory)
        return jsonify(dict_of_rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Получение всех комнат по id общежития
@app.route('/api/rooms/<int:dormitory_id>', methods=['GET'])
def get_rooms_by_dormitory_id(dormitory_id):
    db_service = get_db()
    try:
        # Выполнение запроса для получения всех комнат по id общежития
        query = f"SELECT * FROM rooms WHERE dormitory_id={dormitory_id}"
        rows = db_service.exec_select(query)
        dict_of_rows = rows_to_dict(rows, Room)
        return jsonify(dict_of_rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
