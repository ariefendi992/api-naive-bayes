from email.policy import default
from app.extensions import db
from datetime import datetime, date


class UserModel(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nim = db.Column(db.String(16), nullable=False)
    nama_mhs = db.Column(db.String(128), nullable=False)
    jenis_kelamin = db.Column(db.Enum('laki-laki', 'perempuan'))
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'NIM : {}, Nama : {}'.format(self.nim, self.nama_mhs)


class UserLoginModel(db.Model):
    __tablename__ = 'tb_user_login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
