import datetime
from flask import Blueprint, jsonify, request
from app.lib.http_status_code import *
from app.models.user_model import UserModel, UserLoginModel
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

auth = Blueprint('auth', __name__, url_prefix='/auth')


# register
@auth.post('/register')
def registerUser():
    nim = request.json.get('stambuk')
    nama = request.json.get('nama')
    gender = request.json.get('gender')
    password = request.json.get('password')

    # if len(nim and nama and gender and password) <= 0:
    #     return jsonify({
    #         'error': 'Data tidak boleh kosong',
    #     }), HTTP_400_BAD_REQUEST

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


# Login
@auth.post('/login')
@auth.put('/login')
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
            expireToken = datetime.timedelta(hours=1)
            print(expireToken)
            expireRefreshToken = datetime.timedelta(
                days=30)

            access = create_access_token(
                generateToken, fresh=True, expires_delta=expireToken)
            refresh = create_refresh_token(
                generateToken, expires_delta=expireRefreshToken)

            user_login = UserLoginModel.query.filter_by(
                user_id=sqlUser.id).first()

            if not user_login:
                _userLogin = UserLoginModel(
                    user_id=sqlUser.id, access_token=access, refresh_token=refresh, expire_token_at=expireToken, expire_refresh_at=expireRefreshToken)
                db.session.add(_userLogin)
                db.session.commit()

            else:
                user_login.access_token = access
                user_login.refresh_token = refresh
                user_login.expire_token_at = expireToken
                user_login.expire_refresh_at = expireRefreshToken
                db.session.commit()

            return jsonify({
                'data': {
                    'id': sqlUser.id,
                    'stambuk': sqlUser.nim,
                    'nama': sqlUser.nama_mhs,
                    'token': access,
                    'refresh': refresh,
                    'expire': str(expireToken),
                }
            }), HTTP_200_OK

    return jsonify({
        'error': 'Kesalahan pada autentikasi'
    }), HTTP_401_UNAUTHORIZED


# refresh token
@auth.post('/token-refresh')
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    expireToken = datetime.timedelta(days=7)

    accessToken = create_access_token(
        identity=identity, expires_delta=expireToken)

    sqlQuery = UserLoginModel(user_id=identity.get(
        'id'), refresh_token=accessToken, expire_at=expireToken)
    db.session.commit()

    return jsonify({
        'token': accessToken
    }), HTTP_200_OK


# get all user
@auth.get('/get-all')
@jwt_required()
def getAllUser():
    # current_user = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    sqlQuery = UserModel.query.paginate(page=page, per_page=per_page)

    print(sqlQuery.items)
    data = []
    for i in sqlQuery.items:
        data.append({
            'id': i.id,
            'stambuk': i.nim,
            'nama': i.nama_mhs,
            'gender': i.jenis_kelamin,
            'created_at': i.created_at,
            'updated_at': i.updated_at
        })

    meta = {
        'page': sqlQuery.page,
        'pages': sqlQuery.pages,
        'total_count': sqlQuery.total,
        'prev_page': sqlQuery.prev_num,
        'next_page': sqlQuery.next_num,
        'has_next': sqlQuery.has_next,
        'has_prev': sqlQuery.has_prev,
    }
    return jsonify({
        'data': data,
        'meta': meta,
    }), HTTP_200_OK


# get profil
@auth.get('/get-one')
@jwt_required()
def getOneUser():
    userIdentity = get_jwt_identity()

    print(userIdentity['id'])

    print(userIdentity.items())
    sqlQuery = UserModel.query.filter_by(id=userIdentity.get('id')).first()

    return jsonify({
        'nama': sqlQuery.nama_mhs,
        'nim': sqlQuery.nim
    }), HTTP_200_OK


# edit user
@auth.route('/get-all/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def editUser(id):

    sqlUser = UserModel.query.filter_by(id=id).first()

    print('sqlUser =', sqlUser)

    if not sqlUser:
        return jsonify({
            'msg': 'user tidak ada'
        }), HTTP_404_NOT_FOUND

    stambuk = request.json.get('stambuk')
    nama = request.json.get('nama')
    gender = request.json.get('gender')
    password = request.json.get('password')

    sqlUser.nim = stambuk
    sqlUser.nama_mhs = nama
    sqlUser.jenis_kelamin = gender
    sqlUser.password = password

    db.session.commit()

    return jsonify({
        'id': sqlUser.id,
        'stambuk': sqlUser.nim,
        'nama': sqlUser.nama_mhs,
        'gender': sqlUser.jenis_kelamin,
    }), HTTP_201_CREATED


# Delete User
@auth.delete('/get-all/<int:id>')
@jwt_required()
def deleteUser(id):

    sqlUser = UserModel.query.filter_by(id=id).first()

    if not sqlUser:
        return jsonify({
            'msg': 'akun tidak ditemukan'
        }), HTTP_404_NOT_FOUND

    db.session.delete(sqlUser)
    db.session.commit()

    return jsonify({
        'msg': 'user telah di hapus'
    }), HTTP_204_NO_CONTENT


@auth.route('/logut', methods=['DELETE'])
def logut():
    jti = get_jwt()['jti']
