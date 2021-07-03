from clients.serializers import (
    CreateClientSerializer,
    GeneralClientSerializer,
    DetailedClientSerializer,
    UpdateClientSerializer
)
from clients.models import Client

from rest_framework.viewsets import ModelViewSet


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = DetailedClientSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == 'list':
            serializer_class = GeneralClientSerializer
        elif self.action == 'create':
            serializer_class = CreateClientSerializer
        elif self.action == 'update':
            serializer_class = UpdateClientSerializer
        return serializer_class
