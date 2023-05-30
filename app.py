from flask import Flask, render_template

import jsonworker
from database import DbConnection

app = Flask(__name__)
conn = jsonworker.read_json("connection.json")
db = DbConnection(conn["key"], conn["username"], conn["password"], conn["host"], conn["db"])
db.db_init(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/application')
def applications():
    return "Applications"


if __name__ == "__main__":
    app.run(debug=True)
