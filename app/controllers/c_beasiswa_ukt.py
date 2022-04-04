from itertools import count
from flask import Blueprint, jsonify, request
from app.lib.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_409_CONFLICT
from app.models.beasiswa_model import UktModel
from app.models.user_model import UserModel
from app.models.kampus_model import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.lib.algoritma.algoritma_naive_bayes import CountUkt

ukt = Blueprint('ukt', __name__, url_prefix='/api/v1/beasiswa-ukt')


# get all data
@ukt.route('/', methods=['GET', 'POST'])
@jwt_required()
def getAll():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    sqlQuery = db.session.query(
        UktModel, UserModel, JurusanModel, FakultasModel, SemesterModel)\
        .join(UserModel, JurusanModel, SemesterModel).paginate(
        page=page, per_page=per_page)

    print(sqlQuery.items)

    data = []
    for ukt, user, jur, fak, sms in sqlQuery.items:
        data.append({
            'id': ukt.id,
            'nama': user.nama_mhs,
            'nim': user.nim,
            'nik': ukt.nik,
            'prodi': jur.nama_jurusan,
            'semester': sms.semester,
            'status_mhs': ukt.status_mhs,
            'terima_kip': ukt.penerima_kip,
            'terima_bidik_misi': ukt.penerima_bidik_misi,
            'penghasilan_orang_tua': ukt.penghasilan_orang_tua,
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
    nim = get_jwt_identity().get('nim')
    nik = request.json.get('nik')
    prodi = request.json.get('prodi')
    id_semester = request.json.get('semester')
    status_mhs = request.json.get('status_mhs')
    penerima_kip = request.json.get('kip')
    penerima_bidik_misi = request.json.get('bidik_misi')
    penghasilan_orang_tua = request.json.get('penghasilan_orang_tua')
    tanggungan = request.json.get('tanggungan')
    status_pkh = request.json.get('pkh')
    keputusan = request.json.get('keputusan')

    if UktModel.query.filter_by(id_user=id_user).filter_by(nim=nim).filter_by(nik=nik).first() is not None:
        return jsonify({
            'error': 'Data sudah ada'
        }), HTTP_409_CONFLICT

    sql = UktModel(id_user=id_user,
                   nim=nim,
                   nik=nik,
                   prodi=prodi,
                   id_semester=id_semester,
                   status_mhs=status_mhs,
                   penerima_kip=penerima_kip,
                   penerima_bidik_misi=penerima_bidik_misi,
                   penghasilan_orang_tua=penghasilan_orang_tua,
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
@ukt.post('/tambah-ukt-admin')
@jwt_required()
def addUkt2():
    id_user = request.json.get('id_user')
    nim = request.json.get('stambuk')
    nik = request.json.get('nik')
    prodi = request.json.get('prodi')
    id_semester = request.json.get('semester')
    status_mhs = request.json.get('status_mhs')
    penerima_kip = request.json.get('kip')
    penerima_bidik_misi = request.json.get('bidik_misi')
    penghasilan_orang_tua = request.json.get('penghasilan_orang_tua')
    tanggungan = request.json.get('tanggungan')
    status_pkh = request.json.get('pkh')
    keputusan = request.json.get('keputusan')

    if UktModel.query.filter_by(id_user=id_user).filter_by(nim=nim).filter_by(nik=nik).first() is not None:
        return jsonify({
            'error': 'Data sudah ada'
        }), HTTP_409_CONFLICT

    sql = UktModel(id_user=id_user,
                   nim=nim,
                   nik=nik,
                   prodi=prodi,
                   id_semester=id_semester,
                   status_mhs=status_mhs,
                   penerima_kip=penerima_kip,
                   penerima_bidik_misi=penerima_bidik_misi,
                   penghasilan_orang_tua=penghasilan_orang_tua,
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


# Data Testing
@ukt.route('/testing-ukt', methods=['GET', 'POST'])
def testing_ukt():
    total_data = CountUkt.total_data()
    prob_class = CountUkt.probabilitas_class()
    prodi = CountUkt.atribut_prodi(request.json.get('prodi'))
    semester = CountUkt.atribut_semester(request.json.get('semester'))
    status_mhs = CountUkt.atribut_status_mhs(request.json.get('status_mhs'))
    kip = CountUkt.atribut_kip(request.json.get('penerima_kip'))
    bidik_misi = CountUkt.atribut_bidik_misi(request.json.get('bidik_misi'))
    penghasilan = CountUkt.atribut_penghasilan(request.json.get('penghasilan'))
    tanggungan = CountUkt.atribut_jumlah_tanggungan(
        request.json.get('tanggungan'))
    status_pkh = CountUkt.atribut_pkh(request.json.get('pkh'))

    p_layak = prob_class.get('p_layak') * \
        prodi.get('layak') * semester.get('layak') * \
        status_mhs.get('layak') * kip.get('layak') * \
        bidik_misi.get('layak') * penghasilan.get('layak') * \
        tanggungan.get('layak') * status_pkh.get('layak')
    p_tidak_layak = prob_class.get('p_tidak_layak') * \
        prodi.get('tidak_layak') * semester.get('tidak_layak') * \
        status_mhs.get('tidak_layak') * kip.get('tidak_layak') * \
        bidik_misi.get('tidak_layak') * penghasilan.get('tidak_layak') * \
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
        'atr_penerima_bidik_misi': bidik_misi,
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
    })
