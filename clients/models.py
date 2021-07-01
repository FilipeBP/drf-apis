from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from addresses.models import Address


class Gender(models.TextChoices):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    PREFER_NOT_TO_SAY = 'PNTS'


class Client(models.Model):
    # Números de telefone no Brasil possuem um DDD de dois dígitos entre 1 e 9
    # Seguidos de um 9 inicial, e um dígito de 1 até 9 em sequência.
    phone_regex = RegexValidator(
        regex='^[1-9]{2}9[1-9][0-9]{7}$',
        message='Please enter a valid phone number'
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, null=True, blank=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=4, choices=Gender.choices)
    main_address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, related_name='client')
    secondaries_addressess = models.ManyToManyField(Address, related_name='clients')

    def __str__(self):
        return f'{self.name} {self.last_name}'
