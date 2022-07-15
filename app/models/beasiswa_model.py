from enum import unique
from turtle import pen
from app.extensions import db


# DB UKT
class UktModel(db.Model):
    __tablename__ = 'tb_ukt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_prodi = db.Column(db.Integer, db.ForeignKey(
        'tb_jurusan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_semester = db.Column(db.Integer, db.ForeignKey(
        'tb_semester.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    penerima_kip_bm = db.Column(db.String(32), nullable=False)
    id_penghasilan = db.Column(db.Integer, db.ForeignKey(
        'tb_penghasilan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_tanggungan = db.Column(db.Integer,  db.ForeignKey('tb_tanggungan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status_pkh = db.Column(db.String(32), nullable=False)
    keputusan = db.Column(db.String(32), nullable=True)

    def __repr__(self) -> str:
        return "id_User = {}; status = {}".format(self.id_user, self.keputusan)


class DataTestingUktModel(db.Model):
    __tablename__ = 'tb_ukt_testing'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_prodi = db.Column(db.Integer, db.ForeignKey(
        'tb_jurusan.id'), nullable=False)
    id_semester = db.Column(db.Integer, db.ForeignKey(
        'tb_semester.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    penerima_kip_bm = db.Column(db.String(32), nullable=False)
    id_penghasilan = db.Column(db.Integer, db.ForeignKey(
        'tb_penghasilan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_tanggungan = db.Column(db.Integer, db.ForeignKey(
        'tb_tanggungan.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status_pkh = db.Column(db.String(32), nullable=False)
    keputusan = db.Column(db.String(32), nullable=True)
    
        
    # def __repr__(self):
    #     return f'nama : {self.nama} prodi : {self.prodi}, semester : {self.semester}, status mahasiswa : {self.status_mhs}, status kip : {self.status_kip}, id_penghasilan : {self.id_penghasilan}, id_tanggungan : {self.id_tanggungan}, status pkh : {self.status_pkh}, keputusan : {self.keputusan}'
    
    
class HasilUji(db.Model):
    __tablename__ = 'tb_hasil_ukt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('tb_user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    total_data = db.Column(db.String(16), nullable=False)
    
    