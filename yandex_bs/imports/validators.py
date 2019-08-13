import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidStringValidator:
    def __call__(self, value):
        if not isinstance(value, str):
            raise ValidationError("Should be string instance", code='invalid')
        if not bool(re.match(r'^\w', value)):
            raise ValidationError("Should contain at least one digit or one letter", code='invalid')
