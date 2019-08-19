import copy
import json
import time

from django.urls import reverse
from rest_framework import status

valid_data = {
    "citizens": [
        {
            "citizen_id": 2,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Сергей Иванович",
            "birth_date": "01.04.1997",
            "gender": "male",
            "relatives": [3]
        },
        {
            "citizen_id": 3,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "23.11.1986",
            "gender": "female",
            "relatives": [2]
        }
    ]
}


def test_valid_import(client):
    response = client.post(reverse('create_import'), json.dumps(valid_data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED, response.data


def test_invalid_date_format(client):
    invalid_cases = [
        "1.12.1997",
        "12.1.1997",
        "31.02.1997",
        "12.20.1997",
        "12-1-1997",
        "12.01.1997г",
        "1997",
        "00.05.206",
        "12/12/2012",
        "hello world",
        2012,
        "",
    ]

    for case in invalid_cases:
        data = copy.deepcopy(valid_data)
        data['citizens'][0]['birth_date'] = case
        response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'birth_date' in response.data['citizens'][0]


def test_invalid_string_format(client):
    fields = ["town", "street", "building"]
    invalid_cases = [
        "!@#",
        "",
        "    ",
        "\n",
        "))(*&^%%$#@#$%^&",
        None,
    ]
    for field in fields:
        for case in invalid_cases:
            data = copy.deepcopy(valid_data)
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert field in response.data['citizens'][0]


def test_valid_string_format(client):
    fields = ["town", "street", "building"]
    valid_cases = [
        "1",
        "hello ",
        "   hello 123",
        "h))(*&^%%$#@#$%^&",
    ]
    for field in fields:
        for case in valid_cases:
            data = copy.deepcopy(valid_data)
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED


def test_not_empty_name(client):
    fields = ["name"]
    valid_cases = [
        "1",
        "hello",
        "  (()",
        "!@#",
    ]
    for field in fields:
        for case in valid_cases:
            data = copy.deepcopy(valid_data)
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED


def test_empty_name_invalid(client):
    fields = ["name"]
    invalid_cases = [
        "",
        None,
        []
    ]
    for field in fields:
        for case in invalid_cases:
            data = copy.deepcopy(valid_data)
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert field in response.data['citizens'][0]


def test_non_unique_citizen_ids(client):
    data = copy.deepcopy(valid_data)
    data['citizens'][0]['citizen_id'] = data['citizens'][1]['citizen_id']
    data['citizens'][0]['relatives'] = data['citizens'][1]['relatives'] = []
    response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_incorrect_number_fields(client):
    fields = ["apartment", "citizen_id"]
    invalid_cases = [
        "",
        None,
        [],
        -1,
        -20,
        "test",
        {"name": 1}
    ]
    for field in fields:
        for case in invalid_cases:
            data = copy.deepcopy(valid_data)
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert field in response.data['citizens'][0]


def test_gender_field(client):
    fields = ["gender"]
    invalid_cases = [
        None,
        "",
        "gender",
        "Male",
        "Female",
        "another random string"
    ]
    valid_cases = [
        "male",
        "female"
    ]
    for field in fields:
        for case in invalid_cases:
            data = copy.deepcopy(valid_data)
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert field in response.data['citizens'][0]
        for case in valid_cases:
            data = copy.deepcopy(valid_data)
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED


def test_citizens_relatives_not_exist(client):
    data = copy.deepcopy(valid_data)
    data['citizens'][0]['relatives'] = [5]
    response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_citizens_relatives_not_valid(client):
    data = copy.deepcopy(valid_data)
    data['citizens'][0]['relatives'] = []
    response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_disallow_excess_field(client):
    data = copy.deepcopy(valid_data)
    data['citizens'][0]["excess_field"] = "value"
    response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_retrieve_citizens(client):
    data = copy.deepcopy(valid_data)
    create_response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
    assert create_response.status_code == status.HTTP_201_CREATED
    import_id = create_response.data['data']['import_id']
    retrieve_response = client.get(reverse('retrieve_import', args=[import_id]))
    assert retrieve_response.status_code == status.HTTP_200_OK
    assert retrieve_response.data['data'] == data['citizens']
