from rest_framework import serializers

from clients.models import Client
from users.serializers import UserSerializer
from addresses.serializers import GeneralAddressSerializer


class GeneralClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'user')


class DetailedClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    main_address = GeneralAddressSerializer()
    secondaries_addresses = GeneralAddressSerializer(many=True)

    class Meta:
        model = Client
        fields = '__all__'
