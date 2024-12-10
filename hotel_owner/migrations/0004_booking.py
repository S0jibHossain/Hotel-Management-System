# Generated by Django 5.0.6 on 2024-11-29 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_owner', '0003_hotelowner_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_owner.room')),
            ],
        ),
    ]