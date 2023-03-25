from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.enums import ConnectionType


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    connections = db.relationship('Connection',
                                  foreign_keys='Connection.from_person_id',
                                  backref='from_person', lazy=True)

    # function to return the people who are mutual friends of this Person and other_person
    def mutual_friends(self, other_person):
        other_person_friends = set()
        for connection in other_person.connections:
            if connection.connection_type == ConnectionType.friend:
                other_person_friends.add(connection.to_person)

        self_friends = set()
        for connection in self.connections:
            if connection.connection_type == ConnectionType.friend:
                self_friends.add(connection.to_person)

        return set(self_friends).intersection(other_person_friends)
