# Generated by Django 3.2.5 on 2021-11-18 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animateapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animate',
            name='ani',
            field=models.TextField(blank=True, null=True),
        ),
    ]