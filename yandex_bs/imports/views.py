from collections import defaultdict, Counter

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from yandex_bs.imports.models import ImportObject
from yandex_bs.imports.seralizers import ImportSerializer, CitizenSerializer


class ImportCreateView(APIView):
    def post(self, request):
        import_serializer = ImportSerializer(data=request.data)
        import_serializer.is_valid(raise_exception=True)
        import_instance = import_serializer.save()
        response_data = {
            "data": {
                "import_id": import_instance.id
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class ImportRetrieveView(APIView):
    def get(self, request, import_id):
        import_object = get_object_or_404(ImportObject, pk=import_id)
        citizens = import_object.citizens.order_by('citizen_id')
        citizen_data = CitizenSerializer(citizens, many=True).data
        return Response({"data": citizen_data})


class BirthdaysView(APIView):
    def get(self, request, import_id):
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
