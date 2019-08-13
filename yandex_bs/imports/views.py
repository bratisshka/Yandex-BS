from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from yandex_bs.imports.seralizers import ImportSerializer


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
