# Generated by Django 3.1.7 on 2021-04-10 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0016_auto_20210408_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromMonth', models.DateField(default='--')),
                ('toMonth', models.DateField(default='--')),
                ('amount', models.IntegerField(default=0)),
                ('dueDate', models.DateField(default='--')),
                ('m_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chairman.memberdetail')),
            ],
        ),
    ]