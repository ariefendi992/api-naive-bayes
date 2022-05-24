import datetime
from fileinput import filename
from re import S
from flask import Blueprint, jsonify, request, send_file, url_for
from sqlalchemy import exists
from app.lib.http_status_code import *
from app.models.beasiswa_model import UktModel
from app.models.user_model import UserModel, UserLoginModel
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from app.models.upload_model import UploadPhotoModel
from app.models.kategori_model import JurusanModel
import os

auth = Blueprint('auth', __name__, url_prefix='/auth')

UPLOAD_FOLDER = os.getcwd() + '/app/static/uploads'

# register


@auth.post('/register')
def registerUser():
    nim = request.json.get('stambuk')
    nama = request.json.get('nama')
    id_prodi = request.json.get('id_prodi')
    gender = request.json.get('gender')
    email = request.json.get('email')
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

    sql = UserModel(nim=nim, nama_mhs=nama, id_prodi=id_prodi,
                    jenis_kelamin=gender, email=email, password=passwordHash)
    db.session.add(sql)
    db.session.commit()

    return jsonify({
        'id': sql.id,
        'stambuk': sql.nim,
        'nama': sql.nama_mhs,
        'id_prodi': sql.id_prodi,
        'gender': sql.jenis_kelamin,
        'email': sql.email,
    }), HTTP_201_CREATED


# Login
@auth.post('/login')
@auth.put('/login')
def loginUser():
    # nim = request.json.get('stambuk')
    nim = request.json.get('stambuk')
    password = request.json.get('password')

    # sqlUser = UserModel.query.filter_by(nim=nim).first()
    sqlUser = UserModel.query.join(JurusanModel, UserModel.id_prodi==JurusanModel.id).filter(UserModel.nim==nim).first()
    
    print('sql_user ==', sqlUser)  

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
            expireToken = datetime.timedelta(seconds=3600)
            print(expireToken.seconds)
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
                
            listUser = [] 
            

            return jsonify({
                'data': {
                    'id': sqlUser.id,
                    'stambuk': sqlUser.nim,
                    'nama': sqlUser.nama_mhs,
                    'id_prodi': sqlUser.id_prodi,
                    'token': access,
                    'refresh': refresh,
                    'expire': str(expireToken.seconds),
                    # 'expire': str(expireToken),
                    },
                
            }), HTTP_200_OK

    return jsonify({
        'error': 'Kesalahan pada autentikasi'
    }), HTTP_401_UNAUTHORIZED


# refresh token
@auth.put('/token-refresh')
@auth.post('/token-refresh')
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    expireToken = datetime.timedelta(days=7)

    accessToken = create_access_token(
        identity=identity, expires_delta=expireToken)

    sqlQuery = UserLoginModel.query.filter_by(id=identity.get('id')).first()

    sqlQuery.user_id = identity.get('id')
    sqlQuery.access_token = accessToken
    sqlQuery.expire_token_at = expireToken

    # sqlQuery = UserLoginModel(user_id=identity.get(
    #     'id'), refresh_token=accessToken, expire_token_at=expireToken)
    db.session.commit()

    return jsonify({
        'token': accessToken
    }), HTTP_200_OK


# get all user
@auth.get('/get-all')
# @jwt_required()
def getAllUser():
    # current_user = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    sqlQuery = db.session.query(UserModel).paginate(
        page=page, per_page=per_page)

    data = []
    for i in sqlQuery.items:
        data.append({
            'id': i.id,
            'stambuk': i.nim,
            'nama': i.nama_mhs,
            'gender': i.jenis_kelamin,
            'email': i.email,
            'created_at': str(i.created_at),
            'updated_at': str(i.updated_at)
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


# get user login
@auth.get('/user-login')
def getUserLogin():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    sqlQuery = db.session.query(UserLoginModel, UserModel).join(
        UserModel).paginate(page=page, per_page=per_page)

    data = []
    for ul, u in sqlQuery.items:
        data.append({
            'id': ul.id,
            'nama': u.nama_mhs,
            'token': ul.access_token,
            'refresh_token': ul.refresh_token,
            'login_pertama': str(ul.created_at),
            'terakhir_login': str(ul.modified_at),

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
    sqlQuery = UserModel.query.join(JurusanModel, UserModel.id_prodi == JurusanModel.id).filter_by(id=userIdentity.get('id')).first()

    return jsonify({
        'nama': sqlQuery.nama_mhs,
        'nim': sqlQuery.nim,
        'prodi': sqlQuery.id
    }), HTTP_200_OK


# get user
@auth.get('/get-uid')
def getUserById():

    id = request.args.get('id')
    sqlQuery = UserModel.query.filter_by(id=id).first()

    return jsonify({
        'id': sqlQuery.id,
        'nama': sqlQuery.nama_mhs,
        'nim': sqlQuery.nim,
        'gender': sqlQuery.jenis_kelamin,
        'email': sqlQuery.email,
        'picture': sqlQuery.picture,

    }), HTTP_200_OK


# edit user
@auth.route('/edit-user', methods=['PUT', 'PATCH', 'GET'])
# @jwt_required()
def editUser():
    id = request.args.get('id')
    sqlUser = UserModel.query.filter_by(id=id).first()

    print('sqlUser =', sqlUser)

    if not sqlUser:
        return jsonify({
            'msg': 'user tidak ada'
        }), HTTP_404_NOT_FOUND

    stambuk = request.json.get('stambuk')
    nama = request.json.get('nama')
    gender = request.json.get('gender')
    email = request.json.get('email')
    password = request.json.get('password')

    passwordHash = generate_password_hash(password)

    sqlUser.nim = stambuk
    sqlUser.nama_mhs = nama
    sqlUser.jenis_kelamin = gender
    sqlUser.email = email
    sqlUser.password = passwordHash

    db.session.commit()

    return jsonify({
        'id': sqlUser.id,
        'stambuk': sqlUser.nim,
        'nama': sqlUser.nama_mhs,
        'gender': sqlUser.jenis_kelamin,
        'email': sqlUser.email
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


# Delete User no token
@auth.delete('/delete-user')
def deleteUserByAdmin():
    id = request.args.get('id')
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


# get user is not exist in tb ukt
@auth.get('/user-not-ukt')
def userNotExist():
    sqlQuery = db.session.query(UserModel).filter(
        ~exists(UktModel.id_user).where(UserModel.id == UktModel.id_user)).all()

    data = []
    for user in sqlQuery:
        data.append({
            'id': user.id,
            'nama': user.nama_mhs,
            'stambuk': user.nim
        })

    return jsonify({
        'data': data
    })


@auth.route('/logut', methods=['DELETE'])
def logut():
    jti = get_jwt()['jti']