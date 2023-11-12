from . import views
from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/main')
