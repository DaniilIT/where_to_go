# Generated by Django 4.2 on 2023-05-25 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_alter_place_description_short'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='places', verbose_name='Фотография'),
        ),
    ]