from ast import arg
from sqlalchemy import null, table


class CustomDB():
    def __init__(self, table) -> None:
        self.table = table
    
    def fetch_data(self):
        return self.table.query.all()

    def count_data(self):
        return self.table.query.count()
    
   
        