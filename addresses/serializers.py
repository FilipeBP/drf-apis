from rest_framework import serializers
from addresses.models import Address


class GeneralAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street', 'number', 'complement')


class DetailedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
