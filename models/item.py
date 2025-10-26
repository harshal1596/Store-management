from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), 
                         unique=True, nullable=False)       # Item has only one store but store could have more than one items (one-to-many relationship)
    store = db.relationship("StoreModel", back_populates="items")