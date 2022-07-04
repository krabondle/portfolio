# Generated by Django 3.1 on 2020-10-14 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_ID', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('sensor_type', models.CharField(max_length=2)),
                ('sensor_no', models.CharField(max_length=2)),
                ('sensor_topic', models.CharField(max_length=2)),
                ('Community', models.BooleanField(default=False)),
                ('Home', models.BooleanField(default=False)),
                ('Office', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Value', models.CharField(max_length=10)),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('sensor_ID', models.ForeignKey(db_column='sensor_ID', on_delete=django.db.models.deletion.CASCADE, to='mysite.sensor')),
            ],
        ),
    ]
