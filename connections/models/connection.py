from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.enums import ConnectionType


class Connection(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    from_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    to_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    to_person = db.relationship('Person', foreign_keys=[to_person_id],
                                lazy=True)

    connection_type = db.Column(db.Enum(ConnectionType), nullable=False)
