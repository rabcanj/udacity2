from . import app
from project import controlers, models

@app.route('/')
def hello_world():
    return 'Hello, World!'
