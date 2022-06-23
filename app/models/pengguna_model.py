from app.extensions import db

class PenggunaModel(db.Model):
    __tablename__ = 'tb_pengguna'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), default='user')

    