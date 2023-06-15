import psycopg2
from flask import Flask, render_template, jsonify, g, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import jsonworker
from DBService import DBService
from flask_models import User, RegistrationForm, LoginForm, UserInfoDataLk
from models import Application, Dormitory, Room, RoomAssignmentView, ApplicationView

DATABASE = jsonworker.read_json("connection.json")
app = Flask(__name__)
app.config['SECRET_KEY'] = '*_KTkMh&nbry^>!85s$>coTuN$=]Q9'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


def connect_db():
    """Method for getting new database connection"""
    connection = psycopg2.connect(dbname=DATABASE['db'],
                                  user=DATABASE['username'],
                                  password=DATABASE['password'],
                                  host=DATABASE['host'],
                                  port=DATABASE['port'])
    return DBService(connection)


def rows_to_dict(rows, obj):
    if rows:
        objects_list = [obj(*row) for row in rows]
        objects_dicts = [obj.to_dict() for obj in objects_list]
        return objects_dicts
    else:
        return None


@login_manager.user_loader
def load_user(user_id):
    db_service = connect_db()
    query = f"SELECT userauth.user_id, userauth.login, userauth.\"password\", userinfo.\"name\", " \
            f"userinfo.surname, userinfo.patronymic, userinfo.email, userinfo.phone_number, " \
            f"userinfo.date_of_birth, userinfo.address, userinfo.health_info, userinfo.permissions " \
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
            permissions=row['permissions']
        )
        return user
    return None


@app.route('/')
def index():
    db_service = connect_db()
    try:
        # Выполнение запроса для получения всех общежитий
        query = "SELECT * FROM dormitories"
        rows = db_service.exec_select(query)
        dorms = rows_to_dict(rows, Dormitory)
        return render_template('index.html', regform=RegistrationForm(), logform=LoginForm(), dormitories=dorms)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login')
def login():
    return redirect('/')


def get_applications():
    db_service = connect_db()
    query = ''
    if current_user.permissions == 'user':
        query = f"SELECT * FROM applications_view WHERE user_id={current_user.id}"
    elif current_user.permissions == 'admin':
        query = f"SELECT * FROM applications_view"
    return rows_to_dict(db_service.exec_select(query), ApplicationView)


def get_roomassignments():
    db_service = connect_db()
    query = ''
    if current_user.permissions == 'user':
        query = f"SELECT * FROM assignments_view WHERE user_id={current_user.id}"
    elif current_user.permissions == 'admin':
        query = f"SELECT * FROM assignments_view"
    return rows_to_dict(db_service.exec_select(query), RoomAssignmentView)


@app.route('/lk')
@login_required
def profile():
    try:
        applications = get_applications()
        room_assignments = get_roomassignments()
    except Exception as e:
        return jsonify({"error": str(e)}, 500)
    return render_template('lk.html', user_form=UserInfoDataLk(),
                           applications=applications,
                           assignments=room_assignments)


@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# Маршрут для входа в систему
@app.route('/api/login_user', methods=['POST'])
def auth_user():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        try:
            db_service = connect_db()
            query = f"SELECT user_id FROM userauth WHERE login='{login}' AND password='{password}'"
            user_id = db_service.exec_select(query)
            if user_id:
                user = load_user(user_id[0][0])
                if user:
                    g.user = user  # Загрузка пользователя в контекст
                    login_user(user)
                    # Закрытие курсора
                    db_service.connection.commit()
                    db_service.cursor.close()
            return redirect('/')
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid form data'})


@app.route('/api/add_application/<int:dormitory_id>/<int:room_id>', methods=['POST'])
@login_required
def add_application(dormitory_id, room_id):
    try:
        query = f"INSERT INTO applications (dormitory_id, room_id, user_id) VALUES ({dormitory_id}, {room_id}, {current_user.id})"
        db_service = connect_db()
        db_service.exec_query(query)
        return jsonify({'message': 'Application successfully added'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/change_user_data', methods=['POST'])
@login_required
def update_user_data():
    form = UserInfoDataLk(request.form)
    if form.validate_on_submit():
        name = form.data.get('name')
        surname = form.data.get('surname')
        patronymic = form.data.get('patronymic')
        email = form.data.get('email')
        phone_number = form.data.get('phone_number')
        date_of_birth = form.data.get('date_of_birth')
        address = form.data.get('address')
        health_info = form.data.get('health_info')

        query = f"UPDATE userinfo SET name='{name}', " \
                f"surname='{surname}', patronymic='{patronymic}', " \
                f"email='{email}', phone_number='{phone_number}', " \
                f"date_of_birth='{date_of_birth}', address='{address}', " \
                f"health_info='{health_info}' WHERE user_id = {current_user.id}"
        try:
            db_service = connect_db()
            db_service.exec_query(query)
            g.user = load_user(current_user.id)
            return redirect('/lk')
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
            db_service = connect_db()
            db_service.exec_query(query)
            return redirect('/')
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return redirect('/')


# Получение заявки по id пользователя
@app.route('/api/applications/<int:user_id>', methods=['GET'])
@login_required
def get_application_by_user_id(user_id):
    db_service = connect_db()
    try:
        # Выполнение запроса для получения заявки по id пользователя
        query = f"SELECT * FROM applications WHERE user_id={user_id}"
        rows = db_service.exec_select(query)
        dict_of_rows = rows_to_dict(rows, Application)
        return jsonify(dict_of_rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/change_application_status/<int:application_id>', methods=['POST'])
@login_required
def change_application_status(application_id):
    db_service = connect_db()
    try:
        # Выполнение запроса для получения заявки по id пользователя
        query = f"UPDATE applications SET status=true WHERE application_id={application_id}"
        db_service.exec_query(query)
        return redirect('/lk')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete_assignments/<int:assignment_id>', methods=['POST'])
@login_required
def delete_assignments_row(assignment_id):
    db_service = connect_db()
    try:
        # Выполнение запроса для получения заявки по id пользователя
        query = f"DELETE FROM roomassignments WHERE assignment_id = {assignment_id}"
        db_service.exec_query(query)
        return redirect('/lk')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete_application/<int:application_id>', methods=['POST'])
@login_required
def delete_application_row(application_id):
    db_service = connect_db()
    try:
        # Выполнение запроса для получения заявки по id пользователя
        query = f"DELETE FROM applications WHERE application_id = {application_id}"
        db_service.exec_query(query)
        return redirect('/lk')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Получение всех комнат по id общежития
@app.route('/api/rooms/<int:dormitory_id>', methods=['GET'])
def get_rooms_by_dormitory_id(dormitory_id):
    db_service = connect_db()
    try:
        # Выполнение запроса для получения всех комнат по id общежития
        query = f"SELECT * FROM rooms WHERE dormitory_id={dormitory_id}"
        rows = db_service.exec_select(query)
        dict_of_rows = rows_to_dict(rows, Room)
        return jsonify(dict_of_rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    #app.run(host='192.168.3.102', debug=False)
    app.run(debug=True)
