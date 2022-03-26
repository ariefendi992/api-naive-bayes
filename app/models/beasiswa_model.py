from app.extensions import db


# DB UKT
class UktModel(db.Model):
    __tablename__ = 'tb_ukt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(
        'tb_user.id'), nullable=False)
    id_jurusan = db.Column(db.Integer, db.ForeignKey(
        'tb_jurusan.id'), nullable=False)
    id_fakultas = db.Column(db.Integer, db.ForeignKey(
        'tb_fakultas.id'), nullable=False)
    ipk = db.Column(db.String(8), nullable=False)
    pekerjaan_orang_tua = db.Column(db.String(64), nullable=False)
    penghasilan_orang_tua = db.Column(db.String(64), nullable=False)
    kepemilikan_rumah = db.Column(db.String(64), nullable=False)
    sumber_listrik = db.Column(db.String(32), nullable=False)
    sumber_air = db.Column(db.String(32), nullable=False)
    status_layak = db.Column(db.String(32), nullable=True)

    def __repr__(self) -> str:
        return "id_User = {}; status = {}".format(self.id_user, self.status_layak)


# db Bidik Misi
class BidikMisiModel(db.Model):
    __tablename__ = 'tb_bidik_misi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
