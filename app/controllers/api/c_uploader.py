from flask import Blueprint, jsonify, request
from app.lib.uploader import uploads
from app.models.user_model import UserModel
from app.models.upload_model import UploadPhotoModel
from app.extensions import db

upload = Blueprint('upload', __name__, url_prefix='/upload')


@upload.post('/user-profil/<int:id>')
def uploadPhotoUser(id):

    sqlQuery = UserModel.query.filter_by(id=id).first()
    f = request.files['file']
    # photo = request.form.get('nama_photo')

    upload_data = uploads(f)
    if upload_data['status'] == 'ok':
        newData = UploadPhotoModel(
            id_user=id, photo_path=upload_data["path_file"], photo_name=upload_data['photo_name'])
        db.session.add(newData)
        db.session.commit()
        return jsonify({
            'id_user': sqlQuery.id,
            'nama_photo': upload_data['photo_name']
        })
