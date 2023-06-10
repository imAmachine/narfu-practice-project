from flask import Flask, render_template

import jsonworker
from DBService import DBService

app = Flask(__name__)
conn = jsonworker.read_json("connection.json")
db_service = DBService(db=conn["db"], username=conn["username"], password=conn["password"],
                       host=conn["host"], port=conn["port"])
db_service.service_init(conn["default_schema"])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lk')
def profile():
    return render_template('lk.html')


@app.route('/applications')
def applications():
    db_service.cur.execute('SELECT * FROM applications')
    rows = db_service.cur.fetchall()
    return render_template('applications.html', rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
