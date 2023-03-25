from http import HTTPStatus

import pytest
from tests.factories import ConnectionFactory


def test_can_update_connection(db, testapp):
    ConnectionFactory.create_batch(10)
    db.session.commit()
    res = testapp.patch('/connections/1', json={'connection_type': 'friend'})
    assert res.status_code == HTTPStatus.OK


@pytest.mark.parametrize('connection_type, error_message', [
    pytest.param(None, 'Field may not be null.'),
    pytest.param('NotAConnectionType', 'Invalid enum member NotAConnectionType'),
    pytest.param(1, 'Enum name must be string')
])
def test_update_connection_validations(db, testapp, connection_type, error_message):
    res = testapp.patch('/connections/1', json={'connection_type': connection_type})

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors['connection_type']
