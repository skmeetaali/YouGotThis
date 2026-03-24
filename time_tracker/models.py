from extebsion import db

class time_tracker(db.Model):
    project = db.Column("project", db.String(512))
    weekly_target = db.Column("wtime", db.)
    priority = db.Column("priority", db.Integer)