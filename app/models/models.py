from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Asset(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.String(255), primary_key = True)
    path = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __init__(self, path, name):
        unique_id = str(uuid.uuid4())
        self.id = unique_id
        self.path = f"{path}_{self.id}"
        self.name = name

    def __repr__(self):
        return '<Image %r>' % self.id
    
    def save(self):
        db.session.add(self)
        db.session.commit()