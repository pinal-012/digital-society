# Generated by Django 3.1.7 on 2021-03-30 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0002_watchman_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_pic',
            field=models.FileField(blank=True, default='eventpic_default', upload_to='img/'),
        ),
    ]
