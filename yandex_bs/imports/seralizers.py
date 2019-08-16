from django.db import transaction
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


class PatchCitizenSerializer(CitizenSerializer):
    birth_date = GOSTDateField()

    class Meta:
        model = Citizen
        fields = (
            'town',
            'street',
            'building',
            'apartment',
            'name',
            'birth_date',
            'gender',
            'relatives'
        )

    def validate_relatives(self, relative_list):
        relative_list = list(set(relative_list))
        if Citizen.objects.filter(import_object=self.instance.import_object,
                                  citizen_id__in=relative_list).count() != len(relative_list):
            raise ValidationError("does not exist")
        return relative_list

    def update(self, instance, validated_data):
        new_relatives = validated_data.get('relatives')
        if new_relatives is not None:
            instance_id = instance.citizen_id
            import_object = instance.import_object

            new_relatives_set = set(new_relatives)
            old_relatives_set = set(self.instance.relatives)

            removable_citizen_id_list = list(old_relatives_set.difference(new_relatives_set))
            removable_citizen_list = list(
                Citizen.objects.select_for_update().filter(import_object=import_object,
                                                           citizen_id__in=removable_citizen_id_list))

            with transaction.atomic():
                for citizen in removable_citizen_list:
                    temp_relative_set = set(citizen.relatives)
                    temp_relative_set.remove(instance_id)
                    citizen.relatives = list(temp_relative_set)
                Citizen.objects.bulk_update(removable_citizen_list, ['relatives'])

            appended_citizen_id_list = list(new_relatives_set.difference(old_relatives_set))
            appended_citizen_list = list(
                Citizen.objects.select_for_update().filter(import_object=import_object,
                                                           citizen_id__in=appended_citizen_id_list))
            with transaction.atomic():
                for citizen in appended_citizen_list:
                    temp_relative_set = set(citizen.relatives)
                    temp_relative_set.add(instance_id)
                    citizen.relatives = list(temp_relative_set)
                Citizen.objects.bulk_update(appended_citizen_list, ['relatives'])

        return super().update(instance, validated_data)


class ImportSerializer(serializers.Serializer):
    citizens = CitizenSerializer(many=True)

    def validate_citizens(self, value):
        if len(set([citizen['citizen_id'] for citizen in value])) != len(value):
            raise ValidationError("citizens are not unique in import")
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
