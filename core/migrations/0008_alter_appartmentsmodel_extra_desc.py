# Generated by Django 5.1.6 on 2025-04-15 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_appartmentsmodel_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appartmentsmodel',
            name='extra_desc',
            field=models.TextField(blank=True, db_column='Additional description', default=''),
        ),
    ]
