
class Data(object):
    def __init__(self, table) -> None:
        self.table = table
    
        
    def fetch_data(self):
        return self.table.query.all()


class Data2(object):
    def __init__(self, table) -> None:
        self.table = table
        
    def __repr__(self) -> str:
        return self.table.query.all()    
    
    def cetak(self):
        print('data table = ', self.__repr__())
    

class TotalData(Data):
    def __init__(self, table, layak, tidak) -> None:
        super(TotalData, self).__init__(table)
        self.layak = layak
        self.tidak = tidak
    
    def total_data(self):
        return self.table.query.count()
        
    def data_layak(self):
        return self.table.query.filter(self.layak).count()
    
    def data_tidak(self):
        return self.table.query.filter(self.tidak).count()
    
    def cetak_data(self):
        print('total data = ', self.total_data())
        print('total data layak = ', self.data_layak())
        print('total data tidak layak = ', self.data_tidak())
            
class TotalProdi(TotalData):
    def __init__(self, table, layak, tidak, id) -> None:
        super().__init__(table, layak, tidak)
        self.id = id
        
    def prodi_layak(self):
        return self.table.query.filter(self.layak).count()
    
    def prodi_tidak(self):
        return self.table.query.filter(self.tidak).count()
    
    def cetak_data(self):
        # super().cetak_data()
        print('Prodi layak / data layak = ', self.prodi_layak() / super().data_layak())    
        print('Prodi tidak layak / data tidak layak = ', self.prodi_tidak() / super().data_tidak())    

  