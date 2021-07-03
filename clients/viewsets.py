from clients.services import (
    add_secondary_addresses_to_client,
    remove_secondary_addresses_from_client,
    set_main_address_to_client
)
from utils.serializers import MessageSerializer
from utils.models import Message
from clients.serializers import (
    CreateClientSerializer,
    GeneralClientSerializer,
    DetailedClientSerializer,
    MainAddressSerializer,
    SecondaryAddressesSerializer,
    UpdateClientSerializer
)
from clients.models import Client

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


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

    @swagger_auto_schema(method='put', request_body=MainAddressSerializer)
    @action(methods=['put'], detail=True)
    def set_main_address(self, request, pk=None):
        client = Client.objects.get(pk=pk)

        data = request.data
        main_address_id = data['main_address']

        set_main_address_to_client(client, main_address_id)

        return Response(data)

    @swagger_auto_schema(
        method='put',
        request_body=SecondaryAddressesSerializer,
        responses={200: SecondaryAddressesSerializer, 409: MessageSerializer}
    )
    @action(methods=['put'], detail=True)
    def set_secondary_addresses(self, request, pk=None):
        client = Client.objects.get(pk=pk)

        data = request.data
        secondary_addresses_ids = data['secondary_addresses']

        add_secondary_addresses_to_client(client, secondary_addresses_ids)

        return Response(data)

    @swagger_auto_schema(
        method='delete',
        request_body=SecondaryAddressesSerializer,
        responses={202: MessageSerializer, 404: MessageSerializer}
    )
    @action(methods=['delete'], detail=True)
    def remove_secondary_addresses(self, request, pk=None):
        client = Client.objects.get(pk=pk)

        data = request.data
        secondary_addresses_ids = data['secondary_addresses']

        remove_secondary_addresses_from_client(client, secondary_addresses_ids)

        response_content = MessageSerializer(Message('Secondary addresses removed successfully'))
        return Response(status=status.HTTP_202_ACCEPTED, data=response_content.data)
