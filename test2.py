# from app.lib.algoritma.algoritma_nb_belajar import Data, TotalData, TotalProdi, Data2
from cmath import isnan

from sqlalchemy import null
from app.models.kategori_model import JurusanModel
from app.models.beasiswa_model import UktModel as ukt
from app.lib.algoritma.algoritma_nb import NaiveBayes, ProbProdi, ProbSemester
from app import app 

app.app_context().push()


keputusan = NaiveBayes(ukt, ukt.keputusan)

keputusan.output_data()

prodi = ProbProdi(ukt, ukt.keputusan, ukt.id_prodi == 1)
prodi.output_data()

sms = ProbSemester(ukt, ukt.keputusan, ukt.id_semester == 6)
sms.output_data()

print(keputusan.output_data())
print(prodi.output_data())
print(sms.output_data())

if prodi.output_data()['p_prodi_layak'] == 0 or prodi.output_data()['p_prodi_tidak'] == 0 or \
    sms.output_data()['p_semester_layak'] == 0 or sms.output_data()['p_semester_tidak'] == 0:
        print((prodi.prob_prodi_layak() + 1 )/ (keputusan.prob_keputusan_layak() + 7))
        print(prodi.prob_prodi_tidak() + 1) 
        print((prodi.prob_prodi_tidak() + 1) / (keputusan.prob_keputusan_tidak() + 7)) 
else:
    print('smua mempunyai nilai')

bool = prodi.output_data()['p_prodi_layak'] > prodi.output_data()['p_prodi_tidak']
print(bool)
# def data():
#     data = Data(ukt)
#     return data

# def total_data():
#     total_data = TotalData(ukt, ukt.keputusan == 'layak', ukt.keputusan == 'tidak layak')
#     return total_data


# def total_prodi(prodi = 3):
#     total_prodi = TotalProdi(ukt, ukt.keputusan == 'layak', ukt.keputusan == 'tidak layak', ukt.id_prodi == prodi)
#     return total_prodi

# def data_jurusan():
#     data = Data(JurusanModel)
#     return data

# data().cetak_data()
# total_data().cetak_data()
# total_prodi().cetak_data()

# # data_jurusan().cetak_data()


# def data2():
#     data2 = Data2(JurusanModel)
#     return data2

# data2().cetak()