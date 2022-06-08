from flask import Blueprint, jsonify, request
from app.lib.algoritma.algoritma_nb import NaiveBayes, ProbAtribut
from app.lib.http_status_code import *
from app.models.beasiswa_model import DataTestingUktModel, UktModel
from app.models.user_model import UserLoginModel, UserModel
from app.models.kategori_model import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.lib.algoritma.algoritma_naive_bayes import CountUkt
from app.models.kategori_model import PenghasilanModel
from app.lib.database import CustomDB

ukt = Blueprint('ukt', __name__, url_prefix='/beasiswa-ukt')


# get all data
@ukt.route('/data-record', methods=['GET', 'POST'])
# @jwt_required()
def getAll():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    sqlQuery = db.session.query(
        UktModel, UserModel, JurusanModel, SemesterModel, PenghasilanModel, TanggunganModel)\
        .join(UserModel, JurusanModel, SemesterModel, PenghasilanModel, TanggunganModel).paginate(
        page=page, per_page=per_page)

    data = []
    for ukt, user, jur, sms, peng, tang in sqlQuery.items:
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
            'jml_tanggungan': tang.jml_tanggungan,
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


@ukt.get('/data-record2')
def getAll2():

    sqlQuery = db.session.query(
        UktModel, UserModel, JurusanModel, SemesterModel, PenghasilanModel, TanggunganModel)\
        .join(UserModel, JurusanModel, SemesterModel, PenghasilanModel, TanggunganModel)

    data = []
    for ukt, user, jur, sms, peng, tang in sqlQuery:
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
            'jml_tanggungan': tang.jml_tanggungan,
            'pkh': ukt.status_pkh,
            'keputusan': ukt.keputusan,
        })

    return jsonify({
        'data': data,
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
    id_tanggungan = request.json.get('id_tanggungan')
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
                   id_tanggungan=id_tanggungan,
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
    id_tanggungan = request.json.get('id_tanggungan')
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
                        id_tanggungan=id_tanggungan,
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
        'id_tanggungan': sqlQuery.id_tanggungan,
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
    id_tanggungan = request.json.get('id_tanggungan')
    status_pkh = request.json.get('pkh_kks')
    keputusan = request.json.get('keputusan')

    sqlQuery.nik = nik,
    sqlQuery.id_prodi = prodi,
    sqlQuery.id_semester = id_semester,
    sqlQuery.status_mhs = status_mhs,
    sqlQuery.penerima_kip = penerima_kip,
    sqlQuery.id_penghasilan = id_penghasilan,
    sqlQuery.id_tanggungan = id_tanggungan,
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
        'id_tanggungan': sqlQuery.id_tanggungan,
        'pkh_kks': sqlQuery.status_pkh,
        'kelayakan': sqlQuery.keputusan
    }), HTTP_201_CREATED


# Delete record ukt
@ukt.delete('/delete')
def deleteUkt():
    id = request.args.get('id')
    sqlQuery = UktModel.query.filter_by(id=id).first()

    if not sqlQuery:
        return jsonify({
            'msg': 'id data record tidak ada'
        })

    db.session.delete(sqlQuery)
    db.session.commit()

    return jsonify({
        'msg': 'user telah di hapus'
    }), HTTP_204_NO_CONTENT


# Data Testing 2
@ukt.route('/uji-data', methods=['GET','POST'])
def data_uji():
    id_user = request.json.get('id_user')
    id_prodi = request.json.get('id_prodi')
    id_semester = request.json.get('id_semester')
    statusMhs = request.json.get('status_mhs')
    status_kip = request.json.get('kip_bm')
    id_penghasilan = request.json.get('id_penghasilan')
    id_tanggungan = request.json.get('id_tanggungan')
    pkh = request.json.get('pkh_kks')    
    
    naive_b = NaiveBayes(UktModel, UktModel.keputusan)
    p_prodi = ProbAtribut(UktModel, UktModel.keputusan, UktModel.id_prodi == id_prodi)
    p_sms = ProbAtribut(UktModel, UktModel.keputusan, UktModel.id_semester == id_semester)
    p_status_mhs = ProbAtribut(UktModel, UktModel.keputusan, UktModel.status_mhs == statusMhs)
    p_kip = ProbAtribut(UktModel, UktModel.keputusan, UktModel.penerima_kip_bm == status_kip)
    p_penghasilan = ProbAtribut(UktModel, UktModel.keputusan, UktModel.id_penghasilan == id_penghasilan)
    p_tanggungan = ProbAtribut(UktModel, UktModel.keputusan, UktModel.id_penghasilan == id_tanggungan)
    p_pkh = ProbAtribut(UktModel, UktModel.keputusan, UktModel.status_pkh == pkh)

    p_tidak = {
        'p_prodi_tidak' : round(p_prodi.prob_atr_tidak() / naive_b.prob_keputusan_tidak(), 2),
        'p_sms_tidak' : round(p_sms.prob_atr_tidak() / naive_b.prob_keputusan_tidak(), 2),
        'p_status_mhs_tidak' : round(p_status_mhs.prob_atr_tidak() / naive_b.prob_keputusan_tidak(), 2),
        'p_kip_tidak' : round(p_kip.prob_atr_tidak() / naive_b.prob_keputusan_tidak(), 2),
        'p_penghasilan_tidak' : round(p_penghasilan.prob_atr_tidak() / naive_b.prob_keputusan_tidak(), 2),
        'p_tanggungan_tidak' : round(p_tanggungan.prob_atr_tidak() / naive_b.prob_keputusan_tidak(), 2), 
        'p_pkh_tidak' : round(p_pkh.prob_atr_tidak() / naive_b.prob_keputusan_tidak(), 2), 
        
    }
    
    p_layak = {
        'p_prodi_layak' : round(p_prodi.prob_atr_layak() / naive_b.prob_keputusan_layak(), 2),
        'p_sms_layak' : round(p_sms.prob_atr_layak() / naive_b.prob_keputusan_layak(), 2),
        'p_status_mhs_layak' : round(p_status_mhs.prob_atr_layak() / naive_b.prob_keputusan_layak(), 2),
        'p_kip_layak' : round(p_kip.prob_atr_layak() / naive_b.prob_keputusan_layak(), 2), 
        'p_penghasilan_layak' : round(p_penghasilan.prob_atr_layak() / naive_b.prob_keputusan_layak(), 2), 
        'p_tanggungan_layak' : round(p_tanggungan.prob_atr_layak() / naive_b.prob_keputusan_layak(), 2), 
        'p_pkh_layak' : round(p_pkh.prob_atr_layak() / naive_b.prob_keputusan_layak(), 2), 
    }
    
    if 0 in p_layak.values():
        print('ada')
        p_layak['p_prodi_layak'] = round((p_prodi.prob_atr_layak() + 1) / (naive_b.prob_keputusan_layak() + 7), 2)
        p_layak['p_sms_layak'] = round((p_sms.prob_atr_layak() + 1) / (naive_b.prob_keputusan_layak() + 7), 2)
        p_layak['p_status_mhs_layak'] = round((p_status_mhs.prob_atr_layak() + 1) / (naive_b.prob_keputusan_layak() + 7), 2)
        p_layak['p_kip_layak'] = round((p_kip.prob_atr_layak() + 1) / (naive_b.prob_keputusan_layak() + 7), 2)
        p_layak['p_penghasilan_layak'] = round((p_penghasilan.prob_atr_layak() + 1) / (naive_b.prob_keputusan_layak() + 7), 2)
        p_layak['p_tanggungan_layak'] = round((p_tanggungan.prob_atr_layak() + 1) / (naive_b.prob_keputusan_layak() + 7),2)
        p_layak['p_pkh_layak'] = round((p_pkh.prob_atr_layak() + 1) / (naive_b.prob_keputusan_layak() + 7), 2)
    else: 
        p_layak
        
    if 0 in p_tidak.values():
        p_tidak['p_prodi_tidak'] = round((p_prodi.prob_atr_tidak() + 1) / (naive_b.prob_keputusan_tidak() + 7), 2)
        p_tidak['p_sms_tidak'] = round((p_sms.prob_atr_tidak() + 1) / (naive_b.prob_keputusan_tidak() + 7), 2)
        p_tidak['p_status_mhs_tidak'] = round((p_status_mhs.prob_atr_tidak() + 1) / (naive_b.prob_keputusan_tidak() + 7), 2)
        p_tidak['p_kip_tidak'] = round((p_kip.prob_atr_tidak() + 1) / (naive_b.prob_keputusan_tidak() + 7), 2)
        p_tidak['p_penghasilan_tidak'] = round((p_penghasilan.prob_atr_tidak() + 1) / (naive_b.prob_keputusan_tidak() + 7), 2)
        p_tidak['p_tanggungan_tidak'] = round((p_tanggungan.prob_atr_tidak() + 1) / (naive_b.prob_keputusan_tidak() + 7), 2)
        p_tidak['p_pkh_tidak'] = round((p_pkh.prob_atr_tidak() + 1) / (naive_b.prob_keputusan_tidak() + 7), 2)
    else:
        p_tidak
    
    
    # P(Ci)
    # P(keputusan = layak)
    p_keputusan_layak = naive_b.prob_keputusan_layak() / naive_b.total_data()
    p_keputusan_tidak = naive_b.prob_keputusan_tidak() / naive_b.total_data()    
    
    # P(Ci)
    # P(X | keputusan = layak)
    # p_x_keputusan_layak = p_layak['p_prodi_layak'] * p_layak['p_sms_layak'] * p_layak['p_status_mhs_layak'] * \
    #                   p_layak['p_penghasilan_layak'] * p_layak['p_tanggungan_layak'] * p_layak['p_pkh_layak']
    p_x_keputusan_layak = round(p_layak['p_prodi_layak'], 2) * round(p_layak['p_sms_layak'], 2) * round(p_layak['p_status_mhs_layak'], 2) * \
                      round(p_layak['p_penghasilan_layak'],2) * round(p_layak['p_tanggungan_layak'], 2) * round(p_layak['p_pkh_layak'], 2)
   
    # P(X | keputusan = tidak)
    # p_x_keputusan_tidak = p_tidak['p_prodi_tidak'] * p_tidak['p_sms_tidak'] * p_tidak['p_status_mhs_tidak'] * \
    #                   p_tidak['p_penghasilan_tidak'] * p_tidak['p_tanggungan_tidak'] * p_tidak['p_pkh_tidak']
    p_x_keputusan_tidak = round(p_tidak['p_prodi_tidak'], 2) * round(p_tidak['p_sms_tidak'], 2) * round(p_tidak['p_status_mhs_tidak'], 2) * \
                      round(p_tidak['p_penghasilan_tidak'],2) * round(p_tidak['p_tanggungan_tidak'], 2) * round(p_tidak['p_pkh_tidak'], 2)
    
    # P(X|Ci)*P(Ci)
    # P(X | keputusan = layak * P(Ci) keputusan = layak
    p_x_layak = p_x_keputusan_layak * p_x_keputusan_layak
    
    # P(X | keputusan = tidak * P(Ci) keputusan tidak
    p_x_tidak = p_x_keputusan_tidak * p_x_keputusan_tidak
    
    # 
    if p_x_layak > p_x_tidak:
        msg = 'layak'
        hitung = p_keputusan_layak * 100
        persen = 100 - hitung
    else:
        msg = 'tidak layak'
        hitung = p_keputusan_tidak * 100
        persen = 100 - hitung
        
    if request.method == 'POST':
        user_login = DataTestingUktModel.query.filter_by(
            id_user=id_user).first()
        if not user_login:
            sql = DataTestingUktModel(id_user=id_user, id_prodi = id_prodi, id_semester= id_semester, 
                                status_mhs=statusMhs, penerima_kip_bm=status_kip, id_penghasilan= id_penghasilan,
                                id_tanggungan = id_tanggungan, status_pkh=pkh, keputusan = msg)
            db.session.add(sql)
            db.session.commit()
    
    return jsonify({
        'total_data' : naive_b.total_data(),
        'prob_keputusan_layak' : round(p_keputusan_layak, 2),
        'prob_keputusan_tidak' : round(p_keputusan_tidak, 2),
        'layak': p_layak,
        'tidak': p_tidak,
        'p_x_kep_layak': format(p_x_layak, '.12f'),
        'p_x_kep_tidak': format(p_x_tidak, '.12f'),
        'keputusan' : msg,
        'persen_layak' : round(persen, 2),
        'persen_tidak' : round(hitung, 2),
    }), HTTP_200_OK    
    

# # Data Testing
# @ukt.route('/uji-data', methods=['GET', 'POST'])
# def testing_ukt():
    
    
#     prob_class = CountUkt.probabilitas_class()
#     prodi = CountUkt.atribut_prodi(request.json.get('id_prodi'))
#     semester = CountUkt.atribut_semester(request.json.get('id_semester'))
#     status_mhs = CountUkt.atribut_status_mhs(request.json.get('status_mhs'))
#     kip = CountUkt.atribut_kip(request.json.get('kip_bm'))
#     penghasilan = CountUkt.atribut_penghasilan(
#         request.json.get('id_penghasilan'))
#     tanggungan = CountUkt.atribut_jumlah_tanggungan(
#         request.json.get('tanggungan'))
#     status_pkh = CountUkt.atribut_pkh(request.json.get('pkh_kks'))



    
#     # svae to table data testing
#     id_user = request.json.get('id_user')
#     id_prodi = request.json.get('id_prodi')
#     id_semester = request.json.get('id_semester')
#     statusMhs = request.json.get('status_mhs')
#     status_kip = request.json.get('kip_bm')
#     id_penghasilan = request.json.get('id_penghasilan')
#     jml_tanggungan = request.json.get('tanggungan')
#     pkh = request.json.get('pkh_kks')
    

    
    
    

#     p_layak = prob_class['layak'] * prodi['layak'] * \
#         semester['layak'] * status_mhs['layak'] * \
#         kip['layak'] * penghasilan['layak'] * \
#         tanggungan['layak'] * status_pkh['layak']

#     p_tidak_layak = prob_class.get('tidak_layak') * \
#         prodi.get('tidak_layak') * semester.get('tidak_layak') * \
#         status_mhs.get('tidak_layak') * kip.get('tidak_layak') * \
#         penghasilan['tidak_layak'] * tanggungan.get('tidak_layak') * \
#         status_pkh.get('tidak_layak')

#     if p_layak > p_tidak_layak:
#         msg = 'layak'
#         hitung = prob_class['layak'] * 100
#         total = 100 - hitung
        
#     else:
#         msg = 'tidak layak'
#         hitung = prob_class['tidak_layak'] * 100
#         total = 100 - hitung
        
#     if request.method == 'POST':
#         sql = DataTestingUktModel(id_user=id_user, id_prodi = id_prodi, id_semester= id_semester, 
#                             status_mhs=statusMhs, penerima_kip_bm=status_kip, id_penghasilan= id_penghasilan,
#                             jml_tanggungan = jml_tanggungan, status_pkh=pkh, keputusan = msg)
#         db.session.add(sql)
#         db.session.commit()

#     data = {
#         'total_data': prob_class,
#         'p_class': prob_class,
#         'atr_prodi': prodi,
#         'atr_semester': semester,
#         'atr_status_mhs': status_mhs,
#         'atr_penerima_kip': kip,
#         'atr_penghasilan_orang_tua': penghasilan,
#         'atr_jml_tanggungan': tanggungan,
#         'atr_status_pkh': status_pkh,
#         'probabilitas': {
#             'layak': format(p_layak, '.9f'),
#             'tidak_layak': '{:.9f}'.format(p_tidak_layak)
#         }
#     }

#     return jsonify({
#         'data': data,
#         'kesimpulan': msg,
#         'hitung': {
#             'tidak': hitung,
#             'layak': total
#             }
#     }), HTTP_200_OK
    

# Data Testing Ukt get
@ukt.get('/data-testing')
def fetch_data_testing():
    sql = db.session.query(
                        DataTestingUktModel, UserModel, JurusanModel, SemesterModel, PenghasilanModel, TanggunganModel)\
                        .join(UserModel, JurusanModel, SemesterModel, PenghasilanModel, TanggunganModel).all()
    
    data = {}
    for ukt, user, prodi, sms, penghasilan, tang in sql:
        data.update({
            'id': ukt.id,
            'nama': user.nama_mhs,
            'prodi': prodi.nama_jurusan,
            'semester': sms.semester, 
            'status_mhs': ukt.status_mhs,
            'status_kip': ukt.penerima_kip_bm,
            'penghasilan': penghasilan.ket,
            'tanggungan': tang.jml_tanggungan,
            'status_pkh': ukt.status_pkh,
            'keputusan': ukt.keputusan,
        })     
     
    return jsonify(data), HTTP_200_OK
        