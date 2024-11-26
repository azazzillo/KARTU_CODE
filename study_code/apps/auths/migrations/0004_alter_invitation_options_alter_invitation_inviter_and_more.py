# Generated by Django 4.2.3 on 2024-11-26 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_invitation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={},
        ),
        migrations.AlterField(
            model_name='invitation',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
