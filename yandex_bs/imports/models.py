from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from yandex_bs.imports.validators import ValidStringValidator


class ImportObject(models.Model):
    pass


class Citizen(models.Model):
    citizen_id = models.IntegerField(validators=[MinValueValidator(0)])
    town = models.TextField(validators=[ValidStringValidator()])
    street = models.TextField(validators=[ValidStringValidator()])
    building = models.TextField(validators=[ValidStringValidator()])
    apartment = models.IntegerField(validators=[MinValueValidator(0)])
    name = models.TextField(validators=[MinLengthValidator(0)])
    birth_date = models.DateField()
    import_object = models.ForeignKey(to=ImportObject, related_name='citizens', on_delete=models.CASCADE)

    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    relatives = ArrayField(base_field=models.IntegerField(validators=[MinValueValidator(0)]), blank=True)
