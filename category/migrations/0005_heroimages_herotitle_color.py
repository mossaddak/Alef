# Generated by Django 3.1 on 2023-01-29 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_heroimages_herotitle_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroimages',
            name='herotitle_color',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
