# Generated by Django 2.1 on 2018-10-01 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_management', '0008_participantauthtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantaccountgenerationrequestevent',
            name='generator_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
