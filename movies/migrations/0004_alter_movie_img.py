# Generated by Django 4.1 on 2022-08-15 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='img',
            field=models.CharField(max_length=500),
        ),
    ]
