# Generated by Django 4.2.3 on 2024-11-26 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0004_alter_invitation_options_alter_invitation_inviter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='first_name',
            field=models.CharField(default='None', max_length=50, verbose_name='имя'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='last_name',
            field=models.CharField(default='None', max_length=50, verbose_name='фамилия'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='position_or_group',
            field=models.CharField(blank=True, default='No', max_length=100, null=True),
        ),
    ]
