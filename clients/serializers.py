from rest_framework import serializers

from clients.models import Client
from users.models import User
from addresses.models import Address
from users.serializers import UserSerializer
from addresses.serializers import GeneralAddressSerializer


class GeneralClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'user')


class DetailedClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    main_address = GeneralAddressSerializer(read_only=True)
    secondary_addresses = GeneralAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'


class CreateClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())
    main_address = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Address.objects.all())
    secondary_addresses = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Address.objects.all())

    class Meta:
        model = Client
        fields = '__all__'


class UpdateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'age', 'gender')


class MainAddressSerializer(serializers.ModelSerializer):
    main_address = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Address.objects.all())

    class Meta:
        model = Client
        fields = ('main_address',)


class SecondaryAddressesSerializer(serializers.ModelSerializer):
    secondary_addresses = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=Address.objects.all())

    class Meta:
        model = Client
        fields = ('secondary_addresses',)
