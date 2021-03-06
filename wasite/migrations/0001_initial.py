# Generated by Django 3.2.6 on 2021-08-25 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(max_length=2)),
                ('number', models.CharField(max_length=5)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('date_delete', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('0', 'Not activated'), ('1', 'Activated'), ('2', 'Expired'), ('3', 'Deleted')], max_length=1)),
                ('period', models.CharField(choices=[('1', '1 month'), ('6', '6 months'), ('12', '12 months')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(max_length=7)),
                ('date_create', models.DateTimeField(blank=True, null=True)),
                ('summ', models.FloatField(default=0)),
                ('goods', models.CharField(max_length=100000)),
                ('shop', models.IntegerField()),
                ('emploeye', models.IntegerField()),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wasite.card')),
            ],
        ),
    ]
