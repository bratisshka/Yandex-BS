import json

from rest_framework import status
from rest_framework.reverse import reverse

from yandex_bs.imports.tests.factories import ImportFactory, CitizenFactory


def test_patch_relatives_delete(client):
    import_object = ImportFactory()
    citizen_1 = CitizenFactory(import_object=import_object, citizen_id=1, relatives=[2])
    citizen_2 = CitizenFactory(import_object=import_object, citizen_id=2, relatives=[1])
    url = reverse('patch_citizen', args=[import_object.id, citizen_1.citizen_id])
    data = {
        "relatives": []
    }
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    citizen_2.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['relatives'] == []
    assert citizen_2.relatives == []


def test_patch_relatives_create(client):
    import_object = ImportFactory()
    citizen_1 = CitizenFactory(import_object=import_object, citizen_id=1, relatives=[])
    citizen_2 = CitizenFactory(import_object=import_object, citizen_id=2, relatives=[])
    url = reverse('patch_citizen', args=[import_object.id, citizen_1.citizen_id])
    data = {
        "relatives": [2]
    }
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    citizen_2.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['relatives'] == [2]
    assert citizen_2.relatives == [1]


def test_patch_relatives_create_and_delete(client):
    import_object = ImportFactory()
    citizen_1 = CitizenFactory(import_object=import_object, citizen_id=1, relatives=[2])
    citizen_2 = CitizenFactory(import_object=import_object, citizen_id=2, relatives=[1])
    citizen_3 = CitizenFactory(import_object=import_object, citizen_id=3, relatives=[])
    url = reverse('patch_citizen', args=[import_object.id, citizen_1.citizen_id])
    data = {
        "relatives": [3]
    }
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    citizen_2.refresh_from_db()
    citizen_3.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['relatives'] == [3]
    assert citizen_2.relatives == []
    assert citizen_3.relatives == [1]


def test_patch_relatives_not_exist(client):
    import_object = ImportFactory()
    citizen_1 = CitizenFactory(import_object=import_object, citizen_id=1, relatives=[2])
    citizen_2 = CitizenFactory(import_object=import_object, citizen_id=2, relatives=[1])
    url = reverse('patch_citizen', args=[import_object.id, citizen_1.citizen_id])
    data = {
        "relatives": [3]
    }
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    citizen_2.refresh_from_db()
    citizen_1.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert citizen_1.relatives == [2]
    assert citizen_2.relatives == [1]


def test_patch_citizen_id(client):
    import_object = ImportFactory()
    citizen_1 = CitizenFactory(import_object=import_object, citizen_id=1, relatives=[])
    url = reverse('patch_citizen', args=[import_object.id, citizen_1.citizen_id])
    data = {
        "citizen_id": 2
    }
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    citizen_1.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert citizen_1.citizen_id == 1
