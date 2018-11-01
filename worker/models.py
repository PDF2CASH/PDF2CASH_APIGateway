from django.db import models
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.contrib.auth.models import User


class Worker(User):

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
              '([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})'
              '|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})'
             )
            )
        ]
    )
