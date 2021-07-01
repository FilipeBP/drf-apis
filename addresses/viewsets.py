from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from addresses.models import Address
from addresses.serializers import (
    GeneralAddressSerializer,
    DetailedAddressSerializer
)


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = DetailedAddressSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = GeneralAddressSerializer(queryset, many=True)
        return Response(serialized_data.data)
