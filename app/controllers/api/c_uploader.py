from flask import Blueprint, jsonify, request
from app.lib.uploader import uploads
from app.models.user_model import UserModel
from app.models.upload_model import UploadPhotoModel
from app.extensions import db
from app.lib.http_status_code import *
import string

upload = Blueprint('upload', __name__, url_prefix='/upload')


@upload.post('/user-profil/<int:id>')
def uploadPhotoUser(id):

    sqlQuery = UserModel.query.filter_by(id=id).first()
    f = request.files['image']
    # photo = request.form.get('nama_photo')
    print('nama file ==', f.filename)


    user = sqlQuery.nama_mhs
    # nama_user = user.translate({ord(c): None for c in string.whitespace})
    nama_user = user.replace(" ", "_").lower()

    upload_data = uploads(f, nama_user)
    if upload_data['status'] == 'ok':
        newData = UploadPhotoModel(
            id_user=id, photo_name=upload_data['photo_name'])
        db.session.add(newData)
        db.session.commit()
        return jsonify({
            'id_user': sqlQuery.id,
            'nama_photo': upload_data['photo_name']
        }), HTTP_200_OK
