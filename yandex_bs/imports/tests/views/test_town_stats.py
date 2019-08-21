from unittest import mock

from django.utils.datetime_safe import datetime, date
from rest_framework import status
from rest_framework.reverse import reverse

from yandex_bs.imports.tests.factories import ImportFactory, CitizenFactory


@mock.patch('django.utils.timezone.now')
def test_retrieve_town_stats(now, client):
    now.return_value = datetime(2019, 1, 1, 0, 0, 0)
    import_object = ImportFactory()
    CitizenFactory(import_object=import_object, town='Москва', birth_date=date(2009, 1, 1), relatives=[])
    CitizenFactory(import_object=import_object, town='Москва', birth_date=date(2011, 1, 1), relatives=[])
    CitizenFactory(import_object=import_object, town='Санкт-Петербург', birth_date=date(2012, 1, 1),
                               relatives=[])
    expected_data = [{'town': 'Москва', 'p50': 9.0, 'p75': 9.5, 'p99': 9.98},
                     {'town': 'Санкт-Петербург', 'p50': 7.0, 'p75': 7.0, 'p99': 7.0}]
    url = reverse('town_stats', args=[import_object.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['data'] == expected_data
