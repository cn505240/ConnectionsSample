from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_can_get_mutual_friends(db, testapp):
    # set up test data
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance)
    ConnectionFactory.create_batch(5, to_person=target)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    # issue request for mutual friends
    res = testapp.get('/people/{}/mutual_friends?target_id={}'.format(instance.id, target.id))

    assert res.status_code == HTTPStatus.OK
    res_people = res.json
    assert len(res_people) == 3
    for f in res_people:
        assert f['id'] in expected_mutual_friend_ids
        for field in EXPECTED_FIELDS:
            assert field in f

    # issue another request for mutual friends with the instance and target swapped
    res = testapp.get('/people/{}/mutual_friends?target_id={}'.format(target.id, instance.id))

    assert res.status_code == HTTPStatus.OK
    res_people = res.json
    assert len(res_people) == 3
    for f in res_people:
        assert f['id'] in expected_mutual_friend_ids
        for field in EXPECTED_FIELDS:
            assert field in f
