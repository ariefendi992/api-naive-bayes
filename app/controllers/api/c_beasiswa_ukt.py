from flask import Blueprint, jsonify, request
from app.lib.http_status_code import *
from app.models.beasiswa_model import UktModel
from app.models.user_model import UserModel
from app.models.kategori_model import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.lib.algoritma.algoritma_naive_bayes import CountUkt
from app.models.kategori_model import PenghasilanModel

ukt = Blueprint('ukt', __name__, url_prefix='/beasiswa-ukt')


# get all data
@ukt.route('/data-record', methods=['GET', 'POST'])
# @jwt_required()
def getAll():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    sqlQuery = db.session.query(
        UktModel, UserModel, JurusanModel, SemesterModel, PenghasilanModel)\
        .join(UserModel, JurusanModel, SemesterModel, PenghasilanModel).paginate(
        page=page, per_page=per_page)

    print(sqlQuery.iter_pages())

    data = []
    for ukt, user, jur, sms, peng in sqlQuery.items:
        data.append({
            'id': ukt.id,
            'nama': user.nama_mhs,
            'nim': user.nim,
            'nik': ukt.nik,
            'prodi': jur.nama_jurusan,
            'semester': sms.semester,
            'status_mhs': ukt.status_mhs,
            'terima_kip_bm': ukt.penerima_kip_bm,
            'penghasilan_orang_tua': peng.ket,
            'jml_tanggungan': ukt.jml_tanggungan,
            'pkh': ukt.status_pkh,
            'keputusan': ukt.keputusan,
        })

    meta = {
        'page': sqlQuery.page,
        'pages': sqlQuery.pages,
        'total_count': sqlQuery.total,
        'prev_page': sqlQuery.prev_num,
        'next_page': sqlQuery.next_num,
        'has_next': sqlQuery.has_next,
        'has_prev': sqlQuery.has_prev,
    }

    return jsonify({
        'data': data,
        'meta': meta,
    }), HTTP_200_OK


# create data by user
@ukt.post('/tambah-ukt')
@jwt_required()
def addUkt():
    id_user = get_jwt_identity().get('id')
    nik = request.json.get('nik')
    prodi = request.json.get('prodi')
    id_semester = request.json.get('id_semester')
    status_mhs = request.json.get('status_mhs')
    penerima_kip = request.json.get('kip_bm')
    id_penghasilan = request.json.get('id_penghasilan')
    tanggungan = request.json.get('tanggungan')
    status_pkh = request.json.get('pkh_kks')
    keputusan = request.json.get('keputusan')

    # if UktModel.query.filter_by(id_user=id_user).filter_by(nim=nim).filter_by(nik=nik).first() is not None:
    #     return jsonify({
    #         'error': 'Data sudah ada'
    #     }), HTTP_409_CONFLICT

    sql = UktModel(id_user=id_user,
                   nik=nik,
                   id_prodi=prodi,
                   id_semester=id_semester,
                   status_mhs=status_mhs,
                   penerima_kip_bm=penerima_kip,
                   id_penghasilan=id_penghasilan,
                   jml_tanggungan=tanggungan,
                   status_pkh=status_pkh,
                   keputusan=keputusan,)

    db.session.add(sql)
    db.session.commit()

    return jsonify({
        'id': sql.id,
        'user': sql.id_user,
        'jurusan': sql.prodi,
        'semester': sql.id_semester,
        'keputusan': sql.keputusan,
    }), HTTP_201_CREATED


# create data by admin
@ukt.post('/tambah-data')
# @jwt_required()
def addUkt2():
    id_user = request.json.get('id_user')
    nik = request.json.get('nik')
    prodi = request.json.get('id_prodi')
    id_semester = request.json.get('id_semester')
    status_mhs = request.json.get('status_mhs')
    penerima_kip = request.json.get('kip_bm')
    id_penghasilan = request.json.get('id_penghasilan')
    tanggungan = request.json.get('tanggungan')
    status_pkh = request.json.get('pkh_kks')
    keputusan = request.json.get('keputusan')

    # if UktModel.query.filter_by(id_user=id_user).filter_by(nik=nik).first() is not None:
    #     return jsonify({
    #         'error': 'Data sudah ada'
    #     }), HTTP_409_CONFLICT

    saveData = UktModel(id_user=id_user,
                        nik=nik,
                        id_prodi=prodi,
                        id_semester=id_semester,
                        status_mhs=status_mhs,
                        penerima_kip_bm=penerima_kip,
                        id_penghasilan=id_penghasilan,
                        jml_tanggungan=tanggungan,
                        status_pkh=status_pkh,
                        keputusan=keputusan,)

    db.session.add(saveData)
    db.session.commit()

    return jsonify({
        'id': saveData.id,
        'user': saveData.id_user,
        'prodi': saveData.id_prodi,
        'semester': saveData.id_semester,
        'keputusan': saveData.keputusan,
    }), HTTP_201_CREATED


# get data by id
@ukt.get('/get-one')
def uktGetById():
    id = request.args.get('id')
    sqlQuery = UktModel.query.filter_by(id=id).first()

    return jsonify({
        'id': sqlQuery.id,
        'id_user': sqlQuery.id_user,
        'nik': sqlQuery.nik,
        'id_prodi': sqlQuery.id_prodi,
        'id_sms': sqlQuery.id_semester,
        'status_mhs': sqlQuery.status_mhs,
        'kip_bm': sqlQuery.penerima_kip_bm,
        'id_penghasilan': sqlQuery.id_penghasilan,
        'tanggungan': sqlQuery.jml_tanggungan,
        'pkh_kks': sqlQuery.status_pkh,
        'kelayakan': sqlQuery.keputusan
    }), HTTP_200_OK


# Edit Data record
@ukt.route('/edit-data', methods=['PUT', 'PATCH'])
def editUktData():
    id = request.args.get('id')
    sqlQuery = UktModel.query.filter_by(id=id).first()

    nik = request.json.get('nik')
    prodi = request.json.get('id_prodi')
    id_semester = request.json.get('id_semester')
    status_mhs = request.json.get('status_mhs')
    penerima_kip = request.json.get('kip_bm')
    id_penghasilan = request.json.get('id_penghasilan')
    tanggungan = request.json.get('tanggungan')
    status_pkh = request.json.get('pkh_kks')
    keputusan = request.json.get('keputusan')

    sqlQuery.nik = nik,
    sqlQuery.id_prodi = prodi,
    sqlQuery.id_semester = id_semester,
    sqlQuery.status_mhs = status_mhs,
    sqlQuery.penerima_kip = penerima_kip,
    sqlQuery.id_penghasilan = id_penghasilan,
    sqlQuery.jml_tanggungan = tanggungan,
    sqlQuery.status_pkh = status_pkh,
    sqlQuery.keputusan = keputusan

    db.session.commit()

    return jsonify({
        'id': sqlQuery.id,
        'id_user': sqlQuery.id_user,
        'nik': sqlQuery.nik,
        'id_prodi': sqlQuery.id_prodi,
        'id_sms': sqlQuery.id_semester,
        'status_mhs': sqlQuery.status_mhs,
        'kip_bm': sqlQuery.penerima_kip_bm,
        'id_penghasilan': sqlQuery.id_penghasilan,
        'tanggungan': sqlQuery.jml_tanggungan,
        'pkh_kks': sqlQuery.status_pkh,
        'kelayakan': sqlQuery.keputusan
    }), HTTP_201_CREATED


# Data Testing
@ukt.route('/uji-data', methods=['GET', 'POST'])
def testing_ukt():
    total_data = CountUkt.total_data()
    prob_class = CountUkt.probabilitas_class()
    prodi = CountUkt.atribut_prodi(request.json.get('id_prodi'))
    semester = CountUkt.atribut_semester(request.json.get('id_semester'))
    status_mhs = CountUkt.atribut_status_mhs(request.json.get('status_mhs'))
    kip = CountUkt.atribut_kip(request.json.get('kip_bm'))
    penghasilan = CountUkt.atribut_penghasilan(
        request.json.get('id_penghasilan'))
    tanggungan = CountUkt.atribut_jumlah_tanggungan(
        request.json.get('tanggungan'))
    status_pkh = CountUkt.atribut_pkh(request.json.get('pkh_kks'))

    p_layak = prob_class['p_layak'] * prodi['layak'] * \
        semester['layak'] * status_mhs['layak'] * kip['layak'] * \
        penghasilan['layak'] * tanggungan['layak'] * status_pkh['layak']
    p_tidak_layak = prob_class.get('p_tidak_layak') * \
        prodi.get('tidak_layak') * semester.get('tidak_layak') * \
        status_mhs.get('tidak_layak') * kip.get('tidak_layak') * \
        tanggungan.get('tidak_layak') * status_pkh.get('tidak_layak')

    if p_layak >= p_tidak_layak:
        msg = 'layak'
    else:
        msg = 'tidak layak'

    data = []
    data.append({
        'total_data': total_data,
        'p_class': prob_class,
        'atr_prodi': prodi,
        'atr_semester': semester,
        'atr_status_mhs': status_mhs,
        'atr_penerima_kip': kip,
        'atr_penghasilan_orang_tua': penghasilan,
        'atr_jml_tanggungan': tanggungan,
        'atr_status_pkh': status_pkh,
        'probabilitas': {
            'p_layak': round(p_layak, 2),
            'p_tidak_layak': round(p_tidak_layak, 2)
        }
    })

    return jsonify({
        'data': data,
        'kesimpulan': msg
    }), HTTP_200_OK


# cek ukt
@ukt.get('/cek-ukt')
def cekUkt():
    sqlQuery = UktModel.query.all()

    data = []
    for ukt in sqlQuery:
        data.append({
            'id_user': ukt.id_user
        })

    return jsonify({
        'data': data,
    }), HTTP_200_OK
