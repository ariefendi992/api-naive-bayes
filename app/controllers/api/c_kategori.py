from flask import Blueprint, jsonify, request
from app.lib.database import CustomDB
from app.models.kategori_model import *
from app.extensions import db
from app.lib.http_status_code import *

kategori = Blueprint('kategori', __name__, url_prefix='/kategori')


@kategori.route('/jurusan', methods=['GET', 'POST'])
def jurusan():
    if request.method == 'POST':
        nama_jurusan = request.json.get('jurusan', '')

        if JurusanModel.query.filter_by(nama_jurusan=nama_jurusan).first() is not None:
            return jsonify({
                'msg': 'Data sudah ada'
            })

        data_jurusan = JurusanModel(nama_jurusan=nama_jurusan)
        db.session.add(data_jurusan)
        db.session.commit()

        return jsonify({
            'id': data_jurusan.id,
            'jurusan': data_jurusan.nama_jurusan
        }), HTTP_201_CREATED

    else:
        queryAll = JurusanModel.query.all()
        data = []
        for i in queryAll:
            data.append({
                'id': i.id,
                'jurusan': i.nama_jurusan
            })

        return jsonify({
            'data': data
        }), HTTP_200_OK


@kategori.route('/edit-jurusan', methods=['GET','PUT'])
def edit_jurusan():
    id = request.args.get('id')
    sql = JurusanModel.query.filter_by(id=id).first()

    nama_jurusan = request.json.get('jurusan', '')

    sql.nama_jurusan = nama_jurusan

    db.session.commit()

    return jsonify({
        'id' : sql.id,
        'jurusan' : sql.nama_jurusan
    }), HTTP_201_CREATED


@kategori.delete('jurusan/<int:id>')
def delete_jurusan(id):
    sqlUser = JurusanModel.query.filter_by(id=id).first()

    if not sqlUser:
        return jsonify({
            'msg': 'data tidak ditemukan'
        }), HTTP_404_NOT_FOUND

    db.session.delete(sqlUser)
    db.session.commit()

    return jsonify({
        'msg': 'data telah di hapus'
    }), HTTP_204_NO_CONTENT


@kategori.route('/semester', methods=['GET', 'POST'])
def semester():
    if request.method == 'POST':
        semester = request.json.get('semester')

        if SemesterModel.query.filter_by(semester=semester).first() is not None:
            return jsonify({
                'msg': 'data sudah ada'
            }), HTTP_409_CONFLICT

        dataSemester = SemesterModel(semester=semester)
        db.session.add(dataSemester)
        db.session.commit()

        return jsonify({
            'id': dataSemester.id,
            'semester': dataSemester.semester
        }), HTTP_201_CREATED

    else:
        querySemester = SemesterModel.query.all()

        data = []
        for i in querySemester:
            data.append({
                'id': i.id,
                'semester': i.semester
            })
        return jsonify({
            'data': data
        }), HTTP_200_OK


@kategori.delete('semester/<int:id>')
def delete_semester(id):
    sqlUser = SemesterModel.query.filter_by(id=id).first()

    if not sqlUser:
        return jsonify({
            'msg': 'data tidak ditemukan'
        }), HTTP_404_NOT_FOUND

    db.session.delete(sqlUser)
    db.session.commit()

    return jsonify({
        'msg': 'data telah di hapus'
    }), HTTP_204_NO_CONTENT


@kategori.route('/penghasilan', methods=['POST', 'GET'])
def penghasilan():
    if request.method == 'POST':
        jml_penghasilan = request.json.get('penghasilan')
        ket = request.json.get('keterangan')

        if PenghasilanModel.query.filter_by(jml_penghasilan=jml_penghasilan).first() is not None:
            return jsonify({
                'msg': 'data sudah ada'
            }), HTTP_409_CONFLICT
        simpanData = PenghasilanModel(jml_penghasilan=jml_penghasilan, ket=ket)
        db.session.add(simpanData)
        db.session.commit()

        return jsonify({
            'id': simpanData.id,
            'penghasilan': simpanData.jml_penghasilan,
            'keterangan': simpanData.ket
        }), HTTP_201_CREATED

    else:
        sqlQuery = PenghasilanModel.query.all()

        data = []

        for penghasilan in sqlQuery:
            data.append({
                'id': penghasilan.id,
                'penghasilan': penghasilan.jml_penghasilan,
                'keterangan': penghasilan.ket
            })

        return jsonify({
            'data': data
        }), HTTP_200_OK

@kategori.delete('penghasilan/<int:id>')
def delete_penghasilan(id):
    sqlUser = PenghasilanModel.query.filter_by(id=id).first()

    if not sqlUser:
        return jsonify({
            'msg': 'data tidak ditemukan'
        }), HTTP_404_NOT_FOUND

    db.session.delete(sqlUser)
    db.session.commit()

    return jsonify({
        'msg': 'data telah di hapus'
    }), HTTP_204_NO_CONTENT
        
# jml tanggungan
@kategori.route('/tanggungan', methods=['GET','POST'])
def kat_tanggungan():   
    
    if request.method == 'POST':
        jml_tanggungan = request.json.get('tanggungan')
        data = TanggunganModel(jml_tanggungan=jml_tanggungan)
        
        db.session.add(data)
        db.session.commit()    
            
        return jsonify({
                'id': data.id,
                'tanggungan' : data.jml_tanggungan
            }), HTTP_201_CREATED
    else: 
        data = CustomDB(TanggunganModel)
        
        result = []
        for t in data.fetch_data():
            result.append({
                'id' : t.id,
                'tanggungan' : t.jml_tanggungan
            })
        
        return jsonify({
            'data' : result
        }), HTTP_200_OK

@kategori.delete('tanggungan/<int:id>')
def delete_tanggungan(id):
    sqlUser = TanggunganModel.query.filter_by(id=id).first()

    if not sqlUser:
        return jsonify({
            'msg': 'data tidak ditemukan'
        }), HTTP_404_NOT_FOUND

    db.session.delete(sqlUser)
    db.session.commit()

    return jsonify({
        'msg': 'data telah di hapus'
    }), HTTP_204_NO_CONTENT
        
        
    
    