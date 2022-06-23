from flask import Blueprint, jsonify
from app.lib.database import CustomDB
from app.lib.http_status_code import HTTP_200_OK
from app.models.user_model import UserModel, UserLoginModel
from app.models.beasiswa_model import DataTestingUktModel, HasilUji, UktModel

count_data = Blueprint('count_data', __name__, url_prefix='/total-data')


def countUser():
    sqlQuery = UserModel.query.count()
    return sqlQuery


def countUserLogin():
    sqlQuery = UserLoginModel.query.count()
    return sqlQuery


def countBeasiswaUkt():
    sqlQuery = UktModel.query.count()
    return sqlQuery


def count_data_uji():
    sqlQuery = DataTestingUktModel.query.count()
    return sqlQuery


@count_data.get('/')
def countData():
    total_user = countUser()
    total_user_login = countUserLogin()
    total_penerima_ukt = countBeasiswaUkt()
    total_data_uji = count_data_uji()

    data = []
    data.append({
        'total_user': total_user,
        'total_user_login': total_user_login,
        'total_penerima': {
            'beasiswa_ukt': total_penerima_ukt
        },
        'total_data_uji' : total_data_uji
    
    })

    return jsonify({
        'data': data
    }), HTTP_200_OK

