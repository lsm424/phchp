#encoding=utf-8

from flask import Blueprint

scope_blue = Blueprint('user', __name__, url_prefix='/scope')
from . import scope