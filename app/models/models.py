from flask_sqlalchemy import SQLAlchemy
import uuid
import os

db = SQLAlchemy()


class Asset(db.Model):
    __tablename__ = "images"
    id = db.Column(db.String(255), primary_key=True)
    path = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __init__(self, base_dir, name):
        unique_id = str(uuid.uuid4())
        self.id = unique_id
        self.path = os.path.join(base_dir, unique_id)
        self.name = name

    def __repr__(self):
        return "<Image %r>" % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {"id": self.id, "path": self.path, "name": self.name}
