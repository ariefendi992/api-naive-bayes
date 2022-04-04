from enum import unique
from app.extensions import db


# DB UKT
class UktModel(db.Model):
    __tablename__ = 'tb_ukt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id'), nullable=False)
    nim = db.Column(db.String(32), nullable=False)
    nik = db.Column(db.String(32), nullable=False)
    prodi = db.Column(db.Integer, db.ForeignKey(
        'tb_jurusan.id'), nullable=False)
    id_semester = db.Column(db.Integer, db.ForeignKey(
        'tb_semester.id'), nullable=False)
    status_mhs = db.Column(db.String(32), nullable=False)
    penerima_kip = db.Column(db.String(32), nullable=False)
    penerima_bidik_misi = db.Column(db.String(32), nullable=False)
    penghasilan_orang_tua = db.Column(db.String(64), nullable=False)
    jml_tanggungan = db.Column(db.Integer, nullable=False)
    status_pkh = db.Column(db.String(32), nullable=False)
    keputusan = db.Column(db.String(32), nullable=True)

    def __repr__(self) -> str:
        return "id_User = {}; status = {}".format(self.id_user, self.keputusan)


# db Bidik Misi
class BidikMisiModel(db.Model):
    __tablename__ = 'tb_bidik_misi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
