# Generated by Django 3.1.7 on 2021-04-07 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0012_auto_20210406_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchman',
            name='address',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
