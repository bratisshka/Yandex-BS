import json

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


def test_create_valid_import(client):
    response = client.post(reverse('create_import'), json.dumps(valid_data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED, response.data


def test_create_invalid_date_format(client):
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
        data = valid_data
        data['citizens'][0]['birth_date'] = case
        response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'birth_date' in response.data['citizens'][0]


def test_create_invalid_string_format(client):
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
            data = valid_data
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert field in response.data['citizens'][0]


def test_create_valid_string_format(client):
    fields = ["town", "street", "building"]
    valid_cases = [
        "1",
        "hello ",
        "   hello 123",
        "h))(*&^%%$#@#$%^&",
    ]
    for field in fields:
        for case in valid_cases:
            data = valid_data
            data['citizens'][0][field] = case
            response = client.post(reverse('create_import'), json.dumps(data), content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED
