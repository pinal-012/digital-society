# Generated by Django 3.1.7 on 2021-03-22 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchman',
            name='profile_pic',
            field=models.FileField(blank=True, default='watchman_default_pic.png', upload_to='img/'),
        ),
    ]
