from extension import db

class expense(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    date = db.Column("date", db.Date, nullable = False)
    amount = db.Column("amount", db.Integer, nullable = False)
    item = db.Column("item", db.String(228), nullable = False)
    
    