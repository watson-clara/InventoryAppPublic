from flask import Blueprint

inventory = Blueprint('inventory', __name__)

from .routes import *

