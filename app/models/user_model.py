from email.policy import default
from app.extensions import db
from datetime import datetime
from app.lib.time_zone import utcMakassar


class UserModel(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nim = db.Column(db.String(32), nullable=False)
    nama_mhs = db.Column(db.String(128), nullable=False)
    prodi = db.Column(db.String(128), nullable=False)
    jenis_kelamin = db.Column(db.String(32), nullable=True)
    # jenis_kelamin = db.Column(db.Enum('laki-laki', 'perempuan'))    
    email = db.Column(db.String(128), nullable=False)
    # picture = db.Column(db.String(128), nullable=True)
    berkas = db.Column(db.String(256), nullable=True)
    status_berkas = db.Column(db.String(2), nullable=True, default='0')
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=utcMakassar())
    updated_at = db.Column(db.DateTime, onupdate=utcMakassar())

    def __repr__(self) -> str:
        return 'NIM : {}, Nama : {}'.format(self.nim, self.nama_mhs)


class UserLoginModel(db.Model):
    __tablename__ = 'tb_user_login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,  db.ForeignKey(
        'tb_user.id', ondelete='CASCADE', onupdate='CASCADE'))
    access_token = db.Column(db.String(512), nullable=False)
    refresh_token = db.Column(db.String(512), nullable=False)
    expire_token_at = db.Column(db.Interval, )
    expire_refresh_at = db.Column(db.Interval, )
    created_at = db.Column('created_at', db.DateTime, default=utcMakassar())
    modified_at = db.Column('modified_at', db.DateTime,
                            onupdate=utcMakassar())
