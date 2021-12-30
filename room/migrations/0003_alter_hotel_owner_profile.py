# Generated by Django 4.0 on 2021-12-23 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_hotel_owner_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='owner_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='room.ownerprofile'),
        ),
    ]
