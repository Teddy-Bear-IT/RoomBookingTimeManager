# Generated by Django 5.0.6 on 2024-06-27 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesbooking',
            name='description_booking',
            field=models.CharField(default='Без описания', max_length=500),
        ),
    ]
