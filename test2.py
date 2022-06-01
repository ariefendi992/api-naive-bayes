from app.lib.algoritma.algoritma_nb import Data, TotalData, TotalProdi, Data2
from app.models.kategori_model import JurusanModel
from app.models.beasiswa_model import UktModel as ukt
from app import app 

app.app_context().push()


def data():
    data = Data(ukt)
    return data

def total_data():
    total_data = TotalData(ukt, ukt.keputusan == 'layak', ukt.keputusan == 'tidak layak')
    return total_data


def total_prodi(prodi = 3):
    total_prodi = TotalProdi(ukt, ukt.keputusan == 'layak', ukt.keputusan == 'tidak layak', ukt.id_prodi == prodi)
    return total_prodi

def data_jurusan():
    data = Data(JurusanModel)
    return data

data().cetak_data()
total_data().cetak_data()
total_prodi().cetak_data()

# data_jurusan().cetak_data()


def data2():
    data2 = Data2(JurusanModel)
    return data2

data2().cetak()