# Generated by Django 3.1.7 on 2021-04-10 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0020_auto_20210410_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('checksum', models.CharField(blank=True, max_length=100, null=True)),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='chairman.user')),
            ],
        ),
    ]
