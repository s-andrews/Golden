from Golden import db

class Study (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, unique=True)
    date = db.Column(db.Date)
    description = db.Column(db.Text)

    def __repr__(self):
        return self.title
