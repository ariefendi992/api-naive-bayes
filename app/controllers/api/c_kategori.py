from flask import Blueprint, jsonify, request
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
        })

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
