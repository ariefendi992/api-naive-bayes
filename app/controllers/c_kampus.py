from flask import Blueprint, jsonify, request
from app.models.kampus_model import *
from app.extensions import db
from app.lib.http_status_code import *

kampus = Blueprint('kampus', __name__, url_prefix='/kampus')


@kampus.route('/jurusan', methods=['GET', 'POST'])
def jurusan():

    if request.method == 'POST':
        nama_jurusan = request.json.get('jurusan', '')

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


@kampus.route('/fakultas', methods=['GET', 'POST'])
def fakultas():
    if request.method == 'POST':
        nama_fakultas = request.json.get('fakultas')

        data_fakultas = FakultasModel(nama_fakultas=nama_fakultas)
        db.session.add(data_fakultas)
        db.session.commit()

        return jsonify({
            'id': data_fakultas.id,
            'nama_fakultas': data_fakultas.nama_fakultas
        }), HTTP_201_CREATED

    else:
        queryFakultas = FakultasModel.query.all()

        dataFakultas = []

        for i in queryFakultas:
            dataFakultas.append({
                'id': i.id,
                'fakultas': i.nama_fakultas
            })
        return jsonify({
            'data': dataFakultas
        })


@kampus.route('/semester', methods=['GET', 'POST'])
def fSemester():
    if request.method == 'POST':
        semester = request.json.get('semester')

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
