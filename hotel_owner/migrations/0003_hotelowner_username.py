# Generated by Django 5.0.6 on 2024-11-29 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_owner', '0002_hotelowner'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelowner',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]