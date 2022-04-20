from enum import unique
from app.extensions import db


# DB UKT
class UktModel(db.Model):
    __tablename__ = 'tb_ukt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    nik = db.Column(db.String(32), nullable=False)
    id_prodi = db.Column(db.Integer, db.ForeignKey(
        'tb_jurusan.id'), nullable=False)
    id_semester = db.Column(db.Integer, db.ForeignKey(
        'tb_semester.id'), nullable=False)
    status_mhs = db.Column(db.String(32), nullable=False)
    penerima_kip_bm = db.Column(db.String(32), nullable=False)
    id_penghasilan = db.Column(db.Integer, db.ForeignKey(
        'tb_penghasilan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    jml_tanggungan = db.Column(db.Integer, nullable=False)
    status_pkh = db.Column(db.String(32), nullable=False)
    keputusan = db.Column(db.String(32), nullable=True)

    def __repr__(self) -> str:
        return "id_User = {}; status = {}".format(self.id_user, self.keputusan)


# db KIP
class KipModel(db.Model):
    __tablename__ = 'tb_kip'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
