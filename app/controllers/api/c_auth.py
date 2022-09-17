from dataclasses import replace
import datetime
from fileinput import filename
import json
from turtle import delay
from flask import Blueprint, jsonify, render_template, request, send_file, url_for
from requests import patch
from sqlalchemy import desc, exists, null
from app.lib.http_status_code import *
from app.models.beasiswa_model import UktModel
from app.models.pengguna_model import PenggunaModel
from app.models.upload_model import UploadPhotoModel
from app.models.user_model import UserModel, UserLoginModel
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
import os
from werkzeug.utils import secure_filename
from flask_mail import Message
from app.extensions import mail
import app

auth = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../../static')

UPLOAD_FOLDER = os.getcwd() + '/app/static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# register
@auth.post('/register')
def registerUser():
    nim = request.json.get('stambuk')
    nama = request.json.get('nama')
    prodi = request.json.get('prodi')
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

    if UserModel.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error': 'Email sudah digunakan, silahkan gunakan email yang lain.'
        }), HTTP_409_CONFLICT
    passwordHash = generate_password_hash(password)

    sql = UserModel(nim=nim, nama_mhs=nama, prodi=prodi,
                    jenis_kelamin=gender, email=email, password=passwordHash)
    db.session.add(sql)
    db.session.commit()

    subject = 'Registrasi Akun'
    msg_body = f'Selamat anda telah berhasil melakukan registrasi akun. \
                 \nSilahkan Login dengan menggunakan Stambuk dan Password\n\n -Detail Akun : \
                 \nStambuk : {nim}\nNama : {nama}\nPassword : {password} '
    msg = Message(subject=subject, sender='admin@beasiswa-tuim.site', recipients=[email], body=msg_body)
    mail.send(msg)

    return jsonify({
        'id': sql.id,
        'stambuk': sql.nim,
        'nama': sql.nama_mhs,
        'prodi': sql.prodi,
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

    sqlUser = UserModel.query.filter(UserModel.nim==nim).first()

    
   
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
            expireToken = datetime.timedelta(minutes=60)
            print(expireToken.seconds)
            expireRefreshToken = datetime.timedelta(
                days=30)
            access = create_access_token(
                generateToken, fresh=True, expires_delta=expireToken)
            refresh = create_refresh_token(
                generateToken, expires_delta=expireRefreshToken)

            user_login = UserLoginModel.query.filter_by(
                user_id=sqlUser.id).first()
            
            # select image profil
            imageUser = UploadPhotoModel.query.filter(UploadPhotoModel.id_user == sqlUser.id).order_by(UploadPhotoModel.id.desc()).limit(1).all()

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
                
            # delete imageUser =
            imageUserDel = UploadPhotoModel.query.filter_by(id_user=sqlUser.id).first()
            
            # image_url =   url_for('static', filename='images/'+sqlUser.picture) if sqlUser.picture else None
            nama_photo = ''
            for user in imageUser:
                nama_photo = user.photo_name
            print('nama photo ==== ', nama_photo)
            file = os.path.exists(f'app/static/images/{nama_photo}')
            if file == False:
                db.session.delete(imageUserDel)
                db.session.commit()
                
            image_url = url_for('static', filename='images/'+ nama_photo) if nama_photo else None
            

            return jsonify({
                'data': {
                    'id': sqlUser.id,
                    'stambuk': sqlUser.nim,
                    'nama': sqlUser.nama_mhs,
                    'prodi': sqlUser.prodi,
                    'picture':  image_url if file == True else None,
                    'berkas' : sqlUser.berkas,
                    'status_berkas' : sqlUser.status_berkas,
                    'token': access,
                    'refresh': refresh,
                    'expire': str(expireToken.seconds),
                    },
                
            }), HTTP_200_OK

    return jsonify({
        'error': 'Kesalahan pada autentikasi'
    }), HTTP_401_UNAUTHORIZED


# update user foto by id
@auth.patch('/update-picture')
@auth.put('/update-picture')
def update_profil_picture():
    id = request.args.get('id')
    sqlUser = UserModel.query.filter_by(id=id).first()

    print('sqlUser =', sqlUser)

    if not sqlUser:
        return jsonify({
            'msg': 'user tidak ada'
        }), HTTP_404_NOT_FOUND

    picture = request.files['file']

    if picture and allowed_file(picture.filename):
        filename = secure_filename(picture.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        picture.save(path)
        sqlUser.picture = picture.filename
        db.session.commit()

        return jsonify({
            'id' : sqlUser.id,
            'picture': sqlUser.picture
        }), HTTP_200_OK




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

# get check stambuk
@auth.get('/get-stambuk')
def get_stambuk_by_id():
    sql = UserModel.query.all()

    data = []
    for i in sql:
        data.append({
            'stambuk' : i.nim,
            'nama' : i.nama_mhs
        })

    return jsonify({
        'data' :data
    }), HTTP_200_OK

# get all user
@auth.get('/get-all')
# @jwt_required()
def getAllUser():
    # current_user = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
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
    per_page = request.args.get('per_page', 10, type=int)

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
    sqlQuery = UserModel.query.filter_by(id=userIdentity.get('id')).first()
    imageUser = UploadPhotoModel.query.filter(UploadPhotoModel.id_user == userIdentity['id']).order_by(UploadPhotoModel.id.desc()).limit(1).all()
    
    imageUserDel = UploadPhotoModel.query.filter_by(id_user=userIdentity.get('id')).first()

    nama_photo = None
    for user in imageUser:
        nama_photo = user.photo_name
    print('nama photo ==== ', nama_photo)
    file = os.path.exists(f'app/static/images/{nama_photo}')
    # if file == False:
    #     db.session.delete(imageUserDel)
    #     db.session.commit()

    # image_url =   url_for('static', filename='images/'+ nama_photo) if nama_photo else None
    image_url = url_for('static', filename='images/'+ nama_photo) if nama_photo else None

    return jsonify({
        'id' : sqlQuery.id,
        'nama': sqlQuery.nama_mhs,
        'stambuk': sqlQuery.nim,
        'picture': image_url if file == True else None,
        'email' : sqlQuery.email,
        'gender' : sqlQuery.jenis_kelamin.capitalize(),
        'prodi': sqlQuery.prodi,
        'berkas' : sqlQuery.berkas,
        'status_berkas' : sqlQuery.status_berkas
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
    prodi = request.json.get('prodi')
    gender = request.json.get('gender')
    email = request.json.get('email')
    # password = request.json.get('password')

    # passwordHash = generate_password_hash(password)

    sqlUser.nim = stambuk
    sqlUser.nama_mhs = nama
    sqlUser.jenis_kelamin = gender
    sqlUser.email = email
    # sqlUser.password = passwordHash

    db.session.commit()

    return jsonify({
        'id': sqlUser.id,
        'stambuk': sqlUser.nim,
        'nama': sqlUser.nama_mhs,
        'prodi' :sqlUser.prodi,
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


@auth.route('/get-picture', methods=['GET'])
def picutre():
    sql = UserModel.query.filter_by(id=2).first()

    pic_name = os.path.join(app.createApp().config['UPLOAD_FOLDER'], sql.picture)

    # lokasi = os.getcwd()
    # print(lokasi)
    # print()
    return render_template('index.html', pic_name=pic_name)



# ##################### admin akses web

@auth.post('/regis-pengguna')
@auth.get('/regis-pengguna')
def pengguna_regis():
    username = request.json.get('username')
    password = request.json.get('password')
    status = request.json.get('status')

    if len(password) < 6:
        return jsonify({
            'error': 'Password minimal 6 digit/karakter'
        }), HTTP_400_BAD_REQUEST

    if PenggunaModel.query.filter_by(username=username).first() is not None:
        return jsonify({
            'error': 'Username sudah terdaftar, silahkan login'
        }), HTTP_409_CONFLICT

    passwodHash = generate_password_hash(password)

    sql = PenggunaModel(username=username, password=passwodHash, status=status)

    db.session.add(sql)
    db.session.commit()

    return jsonify({
        'id' : sql.id,
        'username' : sql.username,
        'status' : sql.status
    }), HTTP_201_CREATED


# admin pengguna login
@auth.post('/login-pengguna')
@auth.get('/login-pengguna')
def pengguna_login():
    user = request.json.get('username')
    password = request.json.get('password')
    status = request.json.get('status')

    sql = PenggunaModel.query.filter_by(username=user).first()

    if not sql:
        return jsonify({
            'error' : 'Username tidak ada'
        }), HTTP_401_UNAUTHORIZED

    if sql:
        isPassCorect = check_password_hash(sql.password, password)

        if not isPassCorect:
            return jsonify({
                'error': 'password salah! silahkan cek kembali'
            }), HTTP_401_UNAUTHORIZED

        isStatus = sql.status == status
        if not isStatus:
            return jsonify({
                'error': "Ma'af anda tidak punya hak akses"
            }), HTTP_401_UNAUTHORIZED

        elif isPassCorect and isStatus:
            return jsonify({
                'id' : sql.id,
                'username' : sql.username,
                'status' : sql.status
            }), HTTP_200_OK


        # elif isPassCorect and status == 'admin':
        #     return jsonify({
        #         'id' : sql.id,
        #         'username' : sql.username,
        #         'status' : sql.status
        #     }), HTTP_200_OK

        # elif isPassCorect and status != 'admin':
        #     return jsonify({
        #         'error' : 'Hakses hanya utk admin'
        #     }), HTTP_200_OK

    return jsonify({
        'error' : 'Kesalahan pada autentikasi'
    }), HTTP_401_UNAUTHORIZED

@auth.post('/check-password')
def check_password():
    id = request.args.get('id')
    password = request.json.get('password')

    if len(password) == 0:
         return jsonify({
            'msg' : '**inputan tidak boleh kosong.'
        }), HTTP_404_NOT_FOUND

    # if len(password) < 6:
    #     return jsonify({
    #         'msg' : 'Jumlah password tidak sesuai (minimal 6)'
    #     }), HTTP_404_NOT_FOUND

    sqlUser = UserModel.query.filter_by(id=id).first()

  

    if sqlUser:
        is_pass = check_password_hash(sqlUser.password, password)
        
        if not is_pass and password:
            return jsonify({
                'msg' : 'password salah! harap periksa kembali.'
            }), HTTP_404_NOT_FOUND
        if is_pass:
            return jsonify({
                # 'id' : sqlUser.id,
                # 'nama' : sqlUser.nama_mhs,
                # 'msg' : 'Password sesuai'
                'data': {
                    'id' : sqlUser.id,
                }
                
            }), HTTP_200_OK

    return jsonify({
        'msg' : 'password salah'
    })



@auth.route('/update-password', methods=['PUT'])
def update_password():

    id = request.args.get('id')
    sqlUser = UserModel.query.filter_by(id=id).first()
    if request.method == 'PUT':

        password = request.json.get('password')

        password_hash =  generate_password_hash(password)
        sqlUser.password = password_hash

        db.session.commit()
      
        return jsonify({
            'id' : sqlUser.id,
            'nama' : sqlUser.nama_mhs
        }), HTTP_201_CREATED
        
        
