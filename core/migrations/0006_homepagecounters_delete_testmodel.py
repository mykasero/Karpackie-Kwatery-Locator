# Generated by Django 5.1.6 on 2025-04-07 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_appartmentsmodel_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageCounters',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('appartments_amount', models.IntegerField(db_column='Appartments Amount', default=0)),
                ('locations_amount', models.IntegerField(db_column='Locations Amount', default=0)),
                ('clients_amount', models.IntegerField(db_column='Clients Amount', default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]
