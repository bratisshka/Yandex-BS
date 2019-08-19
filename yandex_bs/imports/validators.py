import re
from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidStringValidator:
    def __call__(self, value):
        if not isinstance(value, str):
            raise ValidationError("Should be string instance", code='invalid')
        if not bool(re.search(r'\w', value)):
            raise ValidationError("Should contain at least one digit or one letter", code='invalid')


class EarlyOrEqualTodayValidator:
    def __call__(self, value):
        if not isinstance(value, date):
            raise ValidationError("should be date instance")
        today = timezone.now().date()
        if value > today:
            raise ValidationError("should be less or equal than today")
