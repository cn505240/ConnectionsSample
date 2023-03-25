from http import HTTPStatus

from flask import Blueprint
from marshmallow import fields
from marshmallow_enum import EnumField
from webargs.flaskparser import use_args

from connections.enums import ConnectionType
from connections.models.connection import Connection
from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema


blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/people/<int:person_id>/mutual_friends')
@use_args({'target_id': fields.Integer()}, locations=('query',))
def get_mutual_friends(args, person_id):
    person = Person.query.filter_by(id=person_id).first()
    target_person = Person.query.filter_by(id=args['target_id']).first()
    if not person or not target_person:
        return '', HTTPStatus.NOT_FOUND

    people_schema = PersonSchema(many=True)
    mutual_friends = person.mutual_friends(target_person)
    return people_schema.jsonify(mutual_friends), HTTPStatus.OK


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connections_schema = ConnectionSchema(many=True)
    connections = Connection.query.all()
    return connections_schema.jsonify(connections), HTTPStatus.OK


@blueprint.route('/connections/<int:connection_id>', methods=['PATCH'])
@use_args({'connection_type': EnumField(ConnectionType)}, locations=('json',))
def update_connection(args, connection_id):
    connection = Connection.query.filter_by(id=connection_id).first()
    if not connection:
        return '', HTTPStatus.NOT_FOUND

    connection.connection_type = args['connection_type']
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED
