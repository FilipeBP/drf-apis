from django.db import models
from django.core.validators import RegexValidator


class Address(models.Model):
    zip_code_regex = RegexValidator(
        regex='^[0-9]{5}-?[0-9]{3}$',
        message='Zip Code must be 00000000 or 00000-000 format.'
    )

    street = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    complement = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=60)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=45)
    zip_code = models.CharField(validators=[zip_code_regex], max_length=9)

    def __str__(self):
        complement = ", " + self.complement if self.complement else ""
        return f'{self.street}, {self.number}{complement}'
