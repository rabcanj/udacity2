from flask import Flask
app = Flask(__name__,
    template_folder='../project/templates',
    )
app.secret_key = 'some secret key'

from project import models
