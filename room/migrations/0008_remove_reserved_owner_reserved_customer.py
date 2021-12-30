# Generated by Django 4.0 on 2021-12-24 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0007_alter_room_hotel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserved',
            name='owner',
        ),
        migrations.AddField(
            model_name='reserved',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner_profiles', related_query_name='owner_profile', to='room.customerprofile'),
        ),
    ]