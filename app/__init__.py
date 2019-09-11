from flask import Flask

app = Flask(__name__, template_folder='../project/templates')
from project import models
