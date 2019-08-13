from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from yandex_bs.imports.models import Citizen, ImportObject
from yandex_bs.imports.serializer_fields import GOSTDateField


class CitizenSerializer(serializers.ModelSerializer):
    birth_date = GOSTDateField()

    class Meta:
        model = Citizen
        fields = (
            'citizen_id',
            'town',
            'street',
            'building',
            'apartment',
            'name',
            'birth_date',
            'gender',
            'relatives'
        )


class ImportSerializer(serializers.Serializer):
    citizens = CitizenSerializer(many=True)

    def validate_citizens(self, value):
        data = {
            citizen['citizen_id']: set(citizen['relatives']) for citizen in value
        }
        for citizen in data.keys():
            for relative_id in data[citizen]:
                relative_set = data.get(relative_id)
                if relative_set is None:
                    raise ValidationError("relatives is not valid (empty relative set)")
                if citizen not in relative_set:
                    raise ValidationError("relatives is not valid")
        return [CitizenSerializer().run_validation(citizen) for citizen in value]

    def create(self, validated_data):
        import_obj = ImportObject.objects.create()
        for citizen in validated_data['citizens']:
            citizen['import_object'] = import_obj
            Citizen.objects.create(**citizen)
        return import_obj
