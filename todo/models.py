from extension import db

class task(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    task = db.Column("task", db.String(1200), nullable = False)
    date = db.Column("date", db.Date, nullable = False)
    expired = db.Column("expired",db.Boolean, nullable = False)