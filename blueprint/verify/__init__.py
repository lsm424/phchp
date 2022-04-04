#encoding=utf-8

from flask import Blueprint

verify_blue = Blueprint('user', __name__, url_prefix='/verify')
from . import verify