from utils.serializers import MessageSerializer
from utils.models import Message
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
from rest_framework import status


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

    @action(methods=['put'], detail=True)
    def set_secondary_addresses(self, request, pk=None):
        client_obj = Client.objects.get(pk=pk)

        data = request.data
        secondary_addresses_ids = data['secondary_addresses']

        if client_obj.main_address_id in secondary_addresses_ids:
            response_content = MessageSerializer(Message('Main address cannot be set as secondary address'))
            return Response(
                data=response_content.data,
                status=status.HTTP_409_CONFLICT
            )

        client_obj.secondary_addresses.add(*secondary_addresses_ids)
        client_obj.save()

        return Response(data)

    @action(methods=['delete'], detail=True)
    def remove_secondary_addresses(self, request, pk=None):
        client_obj = Client.objects.get(pk=pk)

        data = request.data
        secondary_addresses_ids = data['secondary_addresses']

        existing_ids = client_obj.secondary_addresses.filter(id__in=secondary_addresses_ids).values_list('id', flat=True)
        existing_ids = list(existing_ids)
        print(f'{existing_ids = }')
        error_ids = list(set(existing_ids) ^ set(secondary_addresses_ids))
        print(f'{error_ids = }')

        if error_ids:
            response_content = MessageSerializer(Message(f"Secondary address(es): {error_ids} don't exist"))
            return Response(
                data=response_content.data,
                status=status.HTTP_400_BAD_REQUEST
            )

        client_obj.secondary_addresses.remove(*secondary_addresses_ids)
        client_obj.save()

        response_content = MessageSerializer(Message('Secondary addresses removed successfully'))
        return Response(status=status.HTTP_202_ACCEPTED, data=response_content.data)
