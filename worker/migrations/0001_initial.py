# Generated by Django 2.0 on 2018-10-03 01:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=40, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(40)])),
                ('cpf', models.CharField(default=None, max_length=11, unique=True, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.MaxLengthValidator(11), django.core.validators.RegexValidator(regex='([0-9]{2}[\\.]?[0-9]{3}[\\.]?[0-9]{3}[\\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\\.]?[0-9]{3}[\\.]?[0-9]{3}[-]?[0-9]{2})')])),
                ('email', models.EmailField(default=None, max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(100)])),
                ('password', models.CharField(default=None, max_length=30, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(30)])),
            ],
        ),
    ]
