from clients.serializers import (
    GeneralClientSerializer,
    DetailedClientSerializer
)
from clients.models import Client

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = DetailedClientSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = GeneralClientSerializer(queryset, many=True)
        return Response(serialized_data.data)
