from math import prod
from app.lib.algoritma.algoritma_nb import NaiveBayes, ProbAtribut
from app.models.beasiswa_model import UktModel
from app import app 

app.app_context().push()

keputusan = NaiveBayes()
keputusan.table = UktModel
keputusan.filter = UktModel.keputusan
# keputusan.setData(UktModel, UktModel.keputusan)
print(keputusan.output_data())

prodi = ProbAtribut()
prodi.table = UktModel
prodi.filter = UktModel.keputusan
prodi.atribut = UktModel.id_prodi == 3
prodi.atr_layak = 'prob_prodi_layak'
prodi.atr_tidak = 'prob_prodi_tidak'
print('prodi layak = ', prodi.prob_atr_layak())
print('prodi tidak = ', prodi.prob_atr_tidak())
# print(prodi.prob_atr_is_null())

sms = ProbAtribut(UktModel, UktModel.keputusan, UktModel.id_semester)
sms.atr_layak = 'prob_sms_layak'
sms.atr_tidak = 'prob_sms_tidak'
sms.atribut = UktModel.id_semester == 6
print('sms layak = ', sms.prob_atr_layak())
print('sms tidak = ', sms.prob_atr_tidak())
# print(sms.prob_atr_is_null())

if prodi.prob_atr_layak() == 0 or prodi.prob_atr_tidak() == 0 or sms.prob_atr_layak == 0 or sms.prob_atr_tidak() == 0:
    data = {
       'p_prodi_layak': ( prodi.prob_atr_layak() + 1) / (keputusan.prob_keputusan_layak() + 7),
       'p_prodi_tidak': (prodi.prob_atr_tidak() + 1) / (keputusan.prob_keputusan_tidak() + 7),
       'p_sms_layak':( sms.prob_atr_layak() + 1) / (keputusan.prob_keputusan_layak() + 7),
       'p_sms_tidak': (sms.prob_atr_tidak() + 1) / (keputusan.prob_keputusan_tidak() + 7),
    }
    print('laplacian correction = True', data)
else:
    data = {
        'p_prodi_layak': prodi.prob_atr_layak(),
        'p_prodi_tidak': prodi.prob_atr_tidak(),
        'p_sms_layak': sms.prob_atr_layak(),
        'p_sms_tidak': sms.prob_atr_tidak(),
    }
    print('laplacian correction = False',data)