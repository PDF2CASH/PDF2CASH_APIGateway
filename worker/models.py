from django.db import models
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.contrib.auth.models import User


class Worker(User):

    PERMISSION_CHOICES = (
        ('1', 'Worker'),
        ('2', 'Admin'),
    )

    permission = models.CharField(
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

    name = models.CharField(
        max_length=40,
        default='',
        blank=False,
        validators=[
            MinLengthValidator(9),
            MaxLengthValidator(40)
        ]
    )

    cpf = models.CharField(
        max_length=11,
        default='None',
        null=False,
        unique=True,
        blank=False,
        validators=[
            MinLengthValidator(11),
            MaxLengthValidator(11),
            RegexValidator(
                regex=(
                    r'([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})'
                    r'|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})'
                )
            )

        ]
    )
