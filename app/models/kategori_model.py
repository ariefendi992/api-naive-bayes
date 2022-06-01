from app.extensions import db


class JurusanModel(db.Model):
    __tablename__ = 'tb_jurusan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_jurusan = db.Column(db.String(32), nullable=False)

    def __repr__(self) -> str:
        return '(id : {}, Jurusan : {})'.format(self.id, self.nama_jurusan)


class SemesterModel(db.Model):
    __tablename__ = 'tb_semester'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    semester = db.Column(db.String(2), nullable=False)

    def __repr__(self) -> str:
        return 'Semester {}'.format(self.semester)

class PenghasilanModel(db.Model):
    __tablename__ = 'tb_penghasilan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jml_penghasilan = db.Column(db.String(128), nullable=False)
    ket = db.Column(db.String(128), nullable=False)

    def __repr__(self) -> str:
        return 'id : {}; jml_penghasilan : {}; ket : {}'.format(self.id, self.jml_penghasilan, self.ket)
