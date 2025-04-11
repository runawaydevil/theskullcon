from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import routes

__all__ = ['auth_bp'] 