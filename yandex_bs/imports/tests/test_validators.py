from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.utils.datetime_safe import datetime, date

from yandex_bs.imports.validators import ValidStringValidator, EarlyOrEqualTodayValidator


def test_valid_string_validator():
    validator = ValidStringValidator()
    invalid_cases = ["", "!@#", "  ", "<>?><?><?>", "\n"]
    valid_cases = ["1", "a", "fe23e231231", ",.,,123.", "&b.", "/123/", "\\n"]
    for case in invalid_cases:
        with pytest.raises(ValidationError):
            validator(case)

    for case in valid_cases:
        validator(case)


@mock.patch('django.utils.timezone.now')
def test_early_or_equal_today_validator(now):
    validator = EarlyOrEqualTodayValidator()
    now.return_value = datetime(2019, 1, 1, 0, 0, 0)

    with pytest.raises(ValidationError):
        validator(date(2019, 1, 2))

    valid_cases = [
        date(2018, 12, 31),
        date(2019, 1, 1)
    ]

    for case in valid_cases:
        validator(case)
