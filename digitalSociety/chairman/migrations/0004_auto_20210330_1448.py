# Generated by Django 3.1.7 on 2021-03-30 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0003_event_event_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_pic',
            field=models.FileField(blank=True, default='eventpic_default.jpg', upload_to='img/'),
        ),
    ]
