from collections import defaultdict, Counter

import numpy as np
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from yandex_bs.imports.models import ImportObject, Citizen
from yandex_bs.imports.seralizers import ImportSerializer, CitizenSerializer, PatchCitizenSerializer
from yandex_bs.imports.utils import calculate_age


@api_view(['POST'])
def create_import(request):
    import_serializer = ImportSerializer(data=request.data)
    import_serializer.is_valid(raise_exception=True)
    import_instance = import_serializer.save()
    response_data = {
        "data": {
            "import_id": import_instance.id
        }
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view()
def retrieve_import(request, import_id):
    import_object = get_object_or_404(ImportObject, pk=import_id)
    citizens = import_object.citizens.order_by('citizen_id').values_list('citizen_id', 'town', 'street', 'building',
                                                                         'apartment', 'name', 'birth_date', 'gender',
                                                                         'relatives')
    citizen_data = [
        {
            "citizen_id": citizen[0],
            "town": citizen[1],
            "street": citizen[2],
            "building": citizen[3],
            "apartment": citizen[4],
            "name": citizen[5],
            "birth_date": citizen[6].strftime(api_settings.DATE_FORMAT),
            "gender": citizen[7],
            "relatives": citizen[8],
        } for citizen in citizens
    ]
    return Response({"data": citizen_data})


@api_view(['PATCH'])
def patch_citizen(request, import_id, citizen_id):
    import_object = get_object_or_404(ImportObject, pk=import_id)
    citizen_object = get_object_or_404(Citizen, import_object=import_object, citizen_id=citizen_id)
    citizen_serializer = PatchCitizenSerializer(citizen_object, data=request.data, partial=True)
    citizen_serializer.is_valid(raise_exception=True)
    citizen_serializer.save()
    return Response({"data": CitizenSerializer(citizen_object).data})


@api_view()
def retrieve_birthdays(request, import_id):
    import_object = get_object_or_404(ImportObject, pk=import_id)

    birthdays_table = {}

    for citizen_id, birth_date in import_object.citizens.filter(relatives__len__gt=0).values_list('citizen_id',
                                                                                                  'birth_date'):
        birthdays_table[citizen_id] = birth_date.month

    calendar_table = defaultdict(Counter)
    for citizen_id, relatives in import_object.citizens.filter(relatives__len__gt=0).values_list('citizen_id',
                                                                                                 'relatives'):
        for relative in relatives:
            calendar_table[birthdays_table[relative]].update([citizen_id])

    response_data = {str(number): [] for number in range(1, 13)}

    for month_number in range(1, 13):
        for citizen_id in calendar_table[month_number].keys():
            response_data[str(month_number)].append({
                "citizen_id": citizen_id,
                "presents": calendar_table[month_number][citizen_id]
            })

    return Response({"data": response_data})


@api_view()
def retrieve_town_stats(request, import_id):
    import_object = get_object_or_404(ImportObject, pk=import_id)
    town_table = defaultdict(list)
    for town, birth_date in import_object.citizens.values_list('town', 'birth_date'):
        town_table[town].append(calculate_age(birth_date))
    response_data = []
    for town in town_table.keys():
        town_data = {"town": town}
        for percentile_value in [50, 75, 99]:
            town_data["p{}".format(str(percentile_value))] = np.percentile(town_table[town], percentile_value)
        response_data.append(town_data)
    return Response({"data": response_data})
