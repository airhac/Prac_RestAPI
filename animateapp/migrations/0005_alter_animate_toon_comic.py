# Generated by Django 3.2.5 on 2021-11-25 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animateapp', '0004_alter_animate_left_right'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animate',
            name='toon_comic',
            field=models.CharField(choices=[('T', '컷 형식'), ('C', '만화책형식')], default='T', max_length=5),
        ),
    ]
