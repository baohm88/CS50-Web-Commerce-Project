# Generated by Django 4.2.9 on 2024-01-10 09:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='date_crated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]
