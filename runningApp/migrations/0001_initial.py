# Generated by Django 4.2.5 on 2023-10-24 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_name', models.CharField(max_length=100)),
                ('route_description', models.CharField(max_length=500)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RouteStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_order', models.IntegerField(default=0)),
                ('route_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runningApp.route')),
                ('stop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runningApp.stop')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='stops',
            field=models.ManyToManyField(through='runningApp.RouteStop', to='runningApp.stop'),
        ),
        migrations.AddField(
            model_name='route',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
