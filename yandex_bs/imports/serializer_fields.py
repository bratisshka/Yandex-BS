from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateField


class GOSTDateField(DateField):
    """
        Проверяет, что у дня и месяца используются ровно 2 цифры (питон допускает 1).
        Все остальную валидацию пусть делает джанга)
    """

    def to_internal_value(self, value):
        if isinstance(value, str):
            check_value = value.split('.')
            if len(check_value) == 3 and (len(check_value[0]) != 2 or len(check_value[1]) != 2):
                raise ValidationError("date should be the next format: DD-MM-YYYY", code='invalid')

        return super(GOSTDateField, self).to_internal_value(value)
