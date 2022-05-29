from enum import unique
from turtle import pen
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


class DataTestingUktModel(db.Model):
    __tablename__ = 'tb_ukt_testing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(128), nullable=False)
    prodi = db.Column(db.String(64), nullable=False)
    semester = db.Column(db.String(8), nullable=False)
    status_mhs = db.Column(db.String(64), nullable=False)
    status_kip = db.Column(db.String(64), nullable=False)
    penghasilan = db.Column(db.String(128), nullable=False)
    jml_tanggungan = db.Column(db.String(8), nullable=False)
    status_pkh = db.Column(db.String(64), nullable=False)
    keputusan = db.Column(db.String(64), nullable=False)
    
    def __init__(self, id, nama, prodi, semester, status_mhs, status_kip, penghasilan, jml_tanggungan, status_pkh, keputusan):
        self.nama = nama
        self.prodi = prodi
        self.semester = semester
        self.status_mhs = status_mhs
        self.status_kip = status_kip
        self.penghasilan = penghasilan
        self.jml_tanggungan = jml_tanggungan
        self.status_pkh = status_pkh
        self.keputusan = keputusan
        
    def __repr__(self):
        return f'nama : {self.nama} prodi : {self.prodi}, semester : {self.semester}, status mahasiswa : {self.status_mhs}, status kip : {self.status_kip}, penghasilan : {self.penghasilan}, jumlah tanggungan : {self.jml_tanggungan}, status pkh : {self.status_pkh}, keputusan : {self.keputusan}'
    