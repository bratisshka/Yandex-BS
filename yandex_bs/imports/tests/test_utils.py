from unittest import mock

from django.utils.datetime_safe import datetime, date

from yandex_bs.imports.utils import calculate_age


@mock.patch('django.utils.timezone.now')
def test_calculate_age(now):
    now.return_value = datetime(2019, 1, 1, 0, 0, 0)
    assert calculate_age(date(2010, 1, 2)) == 8
    assert calculate_age(date(2010, 1, 1)) == 9
