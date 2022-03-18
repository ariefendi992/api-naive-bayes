import datetime
from flask import Blueprint, jsonify, request
from app.lib.http_status_code import *
from app.models.user_model import UserModel, UserLoginModel
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


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
    }), HTTP_201_CREATED


@auth.post('/login')
def loginUser():
    # nim = request.json.get('stambuk')
    nim = request.json.get('stambuk')
    password = request.json.get('password')

    sqlUser = UserModel.query.filter_by(nim=nim).first()

    if not sqlUser:
        return jsonify({
            'error': 'nim salah! silahkan cek kembali'
        }), HTTP_401_UNAUTHORIZED

    if sqlUser:
        isPassCorrect = check_password_hash(sqlUser.password, password)

        if not isPassCorrect:
            return jsonify({
                'error': 'password salah! silahkan cek kembali'
            }), HTTP_401_UNAUTHORIZED

        elif isPassCorrect:
            generateToken = {
                'id': sqlUser.id,
                'nim': sqlUser.nim,
                'nama': sqlUser.nama_mhs
            }
            expireToken = datetime.timedelta(minutes=20)
            expireRefreshToken = datetime.timedelta(days=30)

            access = create_access_token(
                generateToken, fresh=True, expires_delta=expireToken)
            refresh = create_refresh_token(
                generateToken, expires_delta=expireRefreshToken)

            _userLogin = UserLoginModel(
                user_id=sqlUser.id, refresh_token=refresh, expire_at=expireRefreshToken)

            db.session.add(_userLogin)
            db.session.commit()

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


@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    expireToken = datetime.timedelta(days=7)

    accessToken = create_access_token(
        identity=identity, expires_delta=expireToken)

    sqlQuery = UserLoginModel(user_id=identity.get(
        'id'), refresh_token=accessToken, expire_at=expireToken)

    return jsonify({
        'Refresh Token': accessToken
    })


@auth.get('/get-all')
@jwt_required()
def getAllUser():
    sqlQuery = UserModel.query.all()

    data = []
    for i in sqlQuery:
        data.append({
            'id': i.id,
            'stambuk': i.nim,
            'nama': i.nama_mhs,
            'gender': i.jenis_kelamin,
            'created_at': i.created_at,
            'updated_at': i.updated_at
        })
    return jsonify({
        'data': data
    }), HTTP_200_OK


@auth.get('/get-one')
@jwt_required()
def getOneUser():
    userIdentity = get_jwt_identity()

    print(userIdentity['id'])

    print(userIdentity.items())
    sqlQuery = UserModel.query.filter_by(id=userIdentity.get('id')).first()

    print(sqlQuery)

    return jsonify({
        'user login': userIdentity
    })
