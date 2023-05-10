# Generated by Django 3.1 on 2023-05-07 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='guest_user',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='is_guest_user',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
