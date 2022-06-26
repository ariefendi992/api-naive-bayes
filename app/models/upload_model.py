from app.extensions import db


class UploadPhotoModel(db.Model):
    __tablename__ = 'tb_photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id', ondelete='CASCADE'))
    photo_name = db.Column(db.String(250), nullable=True)


    def __repr__(self) -> str:
        return 'id = {}, id_user = {}, nama foto = {}'.format(self.id, self.id_user, self.photo_name)


# class UploadFileModels(db.Model):
#     __tablename__ = 'tb_file'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_user = db.Column(db.Integer, db.ForeignKey(
#         'tb_user.id', ondelete='CASCADE'))
#     file_path = db.Column(db.String(256), nullable=True)
#     file_name = db.Column(db.String(250), nullable=True)
