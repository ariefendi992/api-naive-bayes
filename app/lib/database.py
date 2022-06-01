class CustomDB():
    def __init__(self, table, db) -> None:
        self.table = table
        self.db = db
        
    def add_data(self):
        return self.table()
    
    def session_add(self):
        return self.db.session.add(self.add_data)
    
    def session_commit(self):
        return self.db.session.commit()
        