# Generated by Django 5.0.6 on 2024-11-29 15:00

import django.db.models.deletion
import hotel_owner.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_owner', '0004_booking'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_owner_bookings', to='hotel_owner.room'),
        ),
        migrations.AlterField(
            model_name='hotelowner',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='hotel_owners/', validators=[hotel_owner.models.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='hotelowner',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]