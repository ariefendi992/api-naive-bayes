from app.extensions import db


class JurusanModel(db.Model):
    __tablename__ = 'tb_jurusan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_jurusan = db.Column(db.String(32), nullable=False)

    def __repr__(self) -> str:
        return 'Jurusan {}'.format(self.nama_jurusan)


class FakultasModel(db.Model):
    __tablename__ = 'tb_fakultas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_fakultas = db.Column(db.String(32), nullable=False)

    def __repr__(self) -> str:
        return 'Fakultas {}'.format(self.nama_fakultas)


class SemesterModel(db.Model):
    __tablename__ = 'tb_semester'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    semester = db.Column(db.String(2), nullable=False)

    def __repr__(self) -> str:
        return 'Semester {}'.format(self.semester)
