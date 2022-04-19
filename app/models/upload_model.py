from app.extensions import db


class UploadPhotoModel(db.Model):
    __tablename__ = 'tb_photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id', ondelete='CASCADE'))
    photo_path = db.Column(db.String(256), nullable=True)
    photo_name = db.Column(db.String(250), nullable=True)


class UploadFileModels(db.Model):
    __tablename__ = 'tb_file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id', ondelete='CASCADE'))
    file_path = db.Column(db.String(256), nullable=True)
    file_name = db.Column(db.String(250), nullable=True)
