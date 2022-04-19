
from app.extensions import db
from app.models.beasiswa_model import UktModel as ukt
from sqlalchemy import case, and_, func


class CountUkt():
    def total_data():
        sql_total_data = ukt.query.count()

        sql_layak = ukt.query.filter(ukt.keputusan == 'layak').count()
        sql_tidak = ukt.query.filter(ukt.keputusan == 'tidak layak').count()

        return {
            'total_data': sql_total_data,
            'layak': sql_layak,
            'tidak_layak': sql_tidak,
        }

    def probabilitas_class():
        sql_layak = ukt.query.filter(ukt.keputusan == 'layak').count(
        ) / CountUkt.total_data().get('total_data')
        sql_tidak = ukt.query.filter(ukt.keputusan == 'tidak layak').count(
        ) / CountUkt.total_data().get('total_data')

        return {
            'p_layak': round(sql_layak, 2),
            'p_tidak_layak': round(sql_tidak, 2),
        }

    def atribut_prodi(prodi):
        sql_layak = ukt.query.filter(
            ukt.prodi == prodi, ukt.keputusan == 'layak').count() / CountUkt.total_data().get('layak')
        sql_tidak = ukt.query.filter(
            ukt.prodi == prodi, ukt.keputusan == 'tidak layak').count() / CountUkt.total_data().get('tidak_layak')

        return ({
            'layak': round(sql_layak, 2),
            'tidak_layak': round(sql_tidak, 2)
        })

    def atribut_semester(semester):
        sql_layak = ukt.query.filter(
            ukt.id_semester == semester, ukt.keputusan == 'layak').count() / CountUkt.total_data().get('layak')
        sql_tidak_layak = ukt.query.filter(
            ukt.id_semester == semester, ukt.keputusan == 'tidak layak').count() / CountUkt.total_data().get('tidak_layak')

        return ({
            'layak': round(sql_layak, 2),
            'tidak_layak': round(sql_tidak_layak, 2),
        })

    def atribut_status_mhs(status):
        sql_layak = ukt.query.filter(ukt.status_mhs == status, ukt.keputusan == 'layak').count(
        ) / CountUkt.total_data().get('layak')

        sql_tidak_layak = ukt.query.filter(ukt.status_mhs == status, ukt.keputusan == 'tidak layak').count(
        ) / CountUkt.total_data().get('tidak_layak')

        return ({
            'layak': round(sql_layak, 2),
            'tidak_layak': round(sql_tidak_layak, 2)
        })

    def atribut_kip(status):
        sql_layak = ukt.query.filter(ukt.penerima_kip_bm == status, ukt.keputusan == 'layak').count(
        ) / CountUkt.total_data().get('layak')
        sql_tidak_layak = ukt.query.filter(ukt.penerima_kip_bm == status, ukt.keputusan == 'tidak layak').count(
        ) / CountUkt.total_data().get('tidak_layak')

        return {
            'layak': round(sql_layak, 2),
            'tidak_layak': round(sql_tidak_layak, 2)
        }

    def atribut_penghasilan(penghasilan):
        # kategori = ""
        # if int(penghasilan) > 2500000:
        #     kategori = 'tinggi'
        # elif int(penghasilan) >= 1500000 and int(penghasilan) <= 2500000:
        #     kategori = 'sedang'
        # elif int(penghasilan) < 1500000:
        #     kategori = 'rendah'

        # caseWHen = case(
        #     (ukt.penghasilan_orang_tua > 2500000, 'tinggi'),
        #     (and_(ukt.penghasilan_orang_tua >= 1500000,
        #      ukt.penghasilan_orang_tua <= 2500000), 'sedang'),
        #     (ukt.penghasilan_orang_tua < 1500000, 'rendah'), else_=''
        # )

        # sql_layak = ukt.query.filter(
        #     caseWHen.label('kategori_penghasilan') == kategori, ukt.keputusan == 'layak').count() / CountUkt.total_data().get('layak')
        # sql_tidak_layak = ukt.query.filter(
        #     caseWHen.label('kategori_penghasilan') == kategori, ukt.keputusan == 'tidak layak').count() / CountUkt.total_data().get('tidak_layak')

        sql_layak = ukt.query.filter(
            ukt.penghasilan_orang_tua == penghasilan, ukt.keputusan == 'layak').count() / CountUkt.total_data().get('layak')
        sql_tidak_layak = ukt.query.filter(
            ukt.penghasilan_orang_tua == penghasilan, ukt.keputusan == 'tidak layak').count() / CountUkt.total_data().get('tidak_layak')

        return {
            'layak': round(sql_layak, 2),
            'tidak_layak': round(sql_tidak_layak, 2)
        }

    def atribut_jumlah_tanggungan(tanggungan):
        if int(tanggungan) > 5:
            tanggungan = 6
        else:
            tanggungan = tanggungan

        case_when = case((ukt.jml_tanggungan > 5, 6), else_=ukt.jml_tanggungan)

        sql_layak = db.session.query(func.count(case_when)).filter(
            ukt.jml_tanggungan == tanggungan, ukt.keputusan == 'layak').scalar() / CountUkt.total_data().get('layak')
        sql_tidak_layak = db.session.query(func.count(case_when)).filter(
            ukt.jml_tanggungan == tanggungan, ukt.keputusan == 'tidak layak').scalar() / CountUkt.total_data().get('tidak_layak')

        return {
            'layak': round(sql_layak, 2),
            'tidak_layak': round(sql_tidak_layak, 2)
        }

    def atribut_pkh(status):
        sql_layak = ukt.query.filter(
            ukt.status_pkh == status, ukt.keputusan == 'layak').count() / CountUkt.total_data().get('layak')
        sql_tidak_layak = ukt.query.filter(
            ukt.status_pkh == status, ukt.keputusan == 'tidak layak').count() / CountUkt.total_data().get('tidak_layak')

        return {
            'layak': round(sql_layak, 2),
            'tidak_layak': round(sql_tidak_layak, 2)
        }
