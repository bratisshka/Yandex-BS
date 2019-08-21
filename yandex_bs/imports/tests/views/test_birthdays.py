import copy

from django.utils.datetime_safe import date
from rest_framework.reverse import reverse

from yandex_bs.imports.tests.factories import ImportFactory, CitizenFactory

expected_data = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": [],
    "9": [],
    "10": [],
    "11": [],
    "12": []
}


def test_retrieve_birthdays(client):
    import_object = ImportFactory()
    CitizenFactory(import_object=import_object, citizen_id=1, birth_date=date(2010, 1, 1), relatives=[2])
    CitizenFactory(import_object=import_object, citizen_id=2, birth_date=date(2010, 2, 1), relatives=[1])
    url = reverse('birthdays', args=[import_object.id])
    data = copy.deepcopy(expected_data)
    data["1"] = [
        {
            "citizen_id": 2,
            "presents": 1
        }
    ]
    data["2"] = [{
        "citizen_id": 1,
        "presents": 1
    }]
    response = client.get(url)
    assert response.data['data'] == data
