# Generated by Django 3.1 on 2023-02-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0008_heroimages_hero_link_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroimages',
            name='hero_link_bgcolor',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]