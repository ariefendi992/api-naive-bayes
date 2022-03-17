from flask import Blueprint, jsonify, request
from app.lib.http_status_code import *
from app.models.user_model import UserModel
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.post('/register')
def registerUser():
    nim = request.json.get('stambuk')
    nama = request.json.get('nama')
    gender = request.json.get('gender')
    password = request.json.get('password')

    if len(password) < 6:
        return jsonify({
            'error': 'Password minimal 6 digit/karakter'
        }), HTTP_400_BAD_REQUEST

    if UserModel.query.filter_by(nim=nim).first() is not None:
        return jsonify({
            'error': 'Nim sudah terdaftar, silahkan login'
        }), HTTP_409_CONFLICT

    passwordHash = generate_password_hash(password)

    sql = UserModel(nim=nim, nama_mhs=nama,
                    jenis_kelamin=gender, password=passwordHash)
    db.session.add(sql)
    db.session.commit()

    return jsonify({
        'id': sql.id,
        'stambuk': sql.nim,
        'nama': sql.nama_mhs,
        'gender': sql.jenis_kelamin,
        'password': sql.password
    }), HTTP_201_CREATED


@auth.get('/')
@jwt_required()
def getAllUser():
    sqlQuery = UserModel.query.all()

    data = []
    for i in sqlQuery:
        data.append({
            'stambuk': i.nim,
            'nama': i.nama_mhs,
            'gender': i.jenis_kelamin,
            'created_at': i.created_at,
            'updated_at': i.updated_at
        })
    return jsonify({
        'data': data
    }), HTTP_200_OK


@auth.post('/login')
def loginUser():
    nim = request.json.get('stambuk')
    password = request.json.get('password')

    sqlUser = UserModel.query.filter_by(nim=nim).first()

    if sqlUser:
        isPassCorrect = check_password_hash(sqlUser.password, password)

        if isPassCorrect:
            access = create_access_token(sqlUser.id)
            refresh = create_refresh_token(sqlUser.id)

            return jsonify({
                'user': {
                    'stambuk': sqlUser.nim,
                    'nama': sqlUser.nama_mhs,
                    'access': access,
                    'refresh': refresh
                }
            }), HTTP_200_OK
    return jsonify({
        'error': 'Kesalahan pada autentikasi'
    }), HTTP_401_UNAUTHORIZED
