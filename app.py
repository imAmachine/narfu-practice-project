import psycopg2
from flask import Flask, render_template, jsonify, g

import jsonworker
from DBService import DBService
from models import UserAuth, Userinfo, Dormitory, Application, RoomAssignment, Room

app = Flask(__name__)
DATABASE = jsonworker.read_json("connection.json")


# Подключение к базе данных
def get_db():
    if 'db' not in g:
        connection = psycopg2.connect(dbname=DATABASE['db'],
                                      user=DATABASE['username'],
                                      password=DATABASE['password'],
                                      host=DATABASE['host'],
                                      port=DATABASE['port'])
        g.db = DBService(connection)
        g.db.service_init(schema='public')
    return g.db


# Закрытие соединения с базой данных после запроса
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.connection.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lk')
def profile():
    return render_template('lk.html')


# Получение заявки по id пользователя
@app.route('/api/applications/<int:user_id>', methods=['GET'])
def get_application_by_user_id(user_id):
    db_service = get_db()

    # Выполнение запроса для получения заявки по id пользователя
    query = f"SELECT * FROM applications WHERE user_id={user_id}"
    try:
        rows = db_service.exec_select(query)
        if rows:
            # Создание объектов Application из результатов запроса
            application_list = [Application(*row) for row in rows]
            # Преобразование объектов Application в словари и возврат в формате JSON
            application_dicts = [app.to_dict() for app in application_list]
            return jsonify(application_dicts)
        else:
            return jsonify({'message': 'No application found for the user'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Получение всех общежитий
@app.route('/api/dormitories', methods=['GET'])
def get_all_dormitories():
    db_service = get_db()

    # Выполнение запроса для получения всех общежитий
    query = "SELECT * FROM dormitories"
    try:
        rows = db_service.exec_select(query)
        if rows:
            # Создание объектов Dormitory из результатов запроса
            dormitory_list = [Dormitory(*row) for row in rows]
            # Преобразование объектов Dormitory в словари и возврат в формате JSON
            dormitory_dicts = [dorm.to_dict() for dorm in dormitory_list]
            return jsonify(dormitory_dicts)
        else:
            return jsonify({'message': 'No dormitories found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Получение всех комнат по id общежития
@app.route('/api/rooms/<int:dormitory_id>', methods=['GET'])
def get_rooms_by_dormitory_id(dormitory_id):
    db_service = get_db()

    # Выполнение запроса для получения всех комнат по id общежития
    query = f"SELECT * FROM rooms WHERE dormitory_id={dormitory_id}"
    try:
        rows = db_service.exec_select(query)
        if rows:
            # Создание объектов Room из результатов запроса
            room_list = [Room(*row) for row in rows]
            # Преобразование объектов Room в словари и возврат в формате JSON
            room_dicts = [room.to_dict() for room in room_list]
            return jsonify(room_dicts)
        else:
            return jsonify({'message': 'No rooms found for the dormitory'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
