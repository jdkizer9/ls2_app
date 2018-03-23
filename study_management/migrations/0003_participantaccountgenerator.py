# Generated by Django 2.0.1 on 2018-03-23 15:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('study_management', '0002_datapoint_metadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantAccountGenerator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('generator_password', models.CharField(max_length=128)),
                ('username_prefix', models.CharField(blank=True, default='', max_length=16)),
                ('username_suffix', models.CharField(blank=True, default='', max_length=16)),
                ('username_random_character_length', models.PositiveSmallIntegerField(default=16)),
                ('password_min_length', models.PositiveSmallIntegerField(default=16)),
                ('password_max_length', models.PositiveSmallIntegerField(default=16)),
                ('number_of_participants_created', models.PositiveSmallIntegerField(default=0)),
                ('max_participants_to_create', models.PositiveSmallIntegerField(default=0)),
                ('study', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='study_management.Study')),
            ],
        ),
    ]
