# Generated by Django 4.1 on 2022-08-15 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='img',
            field=models.TextField(default='http://1.bp.blogspot.com/-3R-zjb0_UK0/T_CnAWhZeAI/AAAAAAAAJ-Q/pwzGrzvRrsw/s1600/avengers_ver14.jpg'),
            preserve_default=False,
        ),
    ]