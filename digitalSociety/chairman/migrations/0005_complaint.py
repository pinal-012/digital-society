# Generated by Django 3.1.7 on 2021-04-02 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0004_auto_20210330_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
