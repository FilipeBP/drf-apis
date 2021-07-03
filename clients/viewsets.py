from clients.serializers import (
    CreateClientSerializer,
    GeneralClientSerializer,
    DetailedClientSerializer,
    UpdateClientSerializer
)
from clients.models import Client

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(methods=['put'], detail=True)
    def set_main_address(self, request, pk=None):
        client_obj = Client.objects.get(pk=pk)

        data = request.data
        main_address_id = data['main_address']

        if client_obj.secondary_addresses.filter(id=main_address_id).exists():
            client_obj.secondary_addresses.remove(main_address_id)

        client_obj.main_address_id = main_address_id
        client_obj.save()

        return Response(data)
