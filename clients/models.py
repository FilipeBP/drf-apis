from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator
from django.contrib.auth import get_user_model
from addresses.models import Address

User = get_user_model()


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
        message='Please enter a valid brazilian phone number.'
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, null=True, blank=True)
    age = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(120)])
    gender = models.CharField(max_length=4, choices=Gender.choices)
    main_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='client', null=True, blank=True)
    secondaries_addresses = models.ManyToManyField(Address, related_name='clients', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
