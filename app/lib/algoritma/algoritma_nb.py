from sqlalchemy import null


class NaiveBayes(object):
    def __init__(self, table=null, filter=null) -> None:
        self.table = table
        self.filter = filter
        
    def setData(self, table, filter):
        self.table = table
        self.filter = filter
        
    def prob_keputusan_layak(self):
        return self.table.query.filter(self.filter == 'layak').count()    
    
    def prob_keputusan_tidak(self):
        return self.table.query.filter(self.filter == 'tidak layak').count()    
    
    def total_data(self):
        return self.prob_keputusan_layak() + self.prob_keputusan_tidak() 
    
        
class ProbAtribut(NaiveBayes):
    def __init__(self, table = null, filter = null, atribut = null) -> None:
        super().__init__(table, filter)
        self.atribut = atribut

        
    def prob_atr_layak(self):
        return self.table.query.filter(self.filter == 'layak', self.atribut).count()
    
    def prob_atr_tidak(self):
        return self.table.query.filter(self.filter == 'tidak layak', self.atribut).count()
    
    