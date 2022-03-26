from flask import Blueprint
from app.models.beasiswa_model import UktModel

ukt = Blueprint('ukt', __name__, url_prefix='/api/v1/beasiswa-ukt')
