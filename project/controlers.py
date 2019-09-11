from app import app
import sqlalchemy as db
from flask import render_template


def get_connection():
    engine = db.create_engine('sqlite:///census.sqlite')
    return engine.connect()


@app.route('/index')
def index():
    connection = get_connection()
    result = connection.execute("select * from CATEGORY")
    for row in result:
        print("username:", row['name'])
    connection.close()
    return render_template('index.html', user={})
