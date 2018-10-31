from django.db import models
from django.core.validators import (
        RegexValidator,
        MinLengthValidator,
        MaxLengthValidator,
        )

# Create your models here.

class Worker(models.Model):
    PERMISSION_CHOICES = (
        ('1', 'Worker'),
        ('2', 'Admin'),
    )

    name = models.CharField(
            max_length=40,
            default=None,
            null=False,
            blank=False,
            validators=[
                MinLengthValidator(9),
                MaxLengthValidator(40)
                ]
            )

    cpf = models.CharField(
            max_length=11,
            default=None,
            null=False,
            unique=True,
            blank=False,
            validators=[
                MinLengthValidator(11),
                MaxLengthValidator(11),
                RegexValidator(
                    regex=(
                        '([0-9]{2}[.]?[0-9]{3}[.]?[0-9]{3}[/]?[0-9]{4}[-]?[0-9]{2})'
                        '|([0-9]{3}[.]?[0-9]{3}[.]?[0-9]{3}[-]?[0-9]{2})'
                        )
                    )
                ]
            )

    email = models.EmailField(
            max_length=100,
            default=None,
            null=False,
            unique=True,
            blank=False,
            validators=[
                MinLengthValidator(10),
                MaxLengthValidator(100)
                ]
            )

    password = models.CharField (
            max_length=30,
            default=None,
            null=False,
            blank=False,
            validators=[
                MinLengthValidator(6),
                MaxLengthValidator(30)
                ]
            )
    
    permission = models.CharField (
        default=1,
        max_length=1,
        null=False,
        blank=False,
        choices=PERMISSION_CHOICES,
            validators=[
                MinLengthValidator(1),
                MaxLengthValidator(1)
                ]
    )