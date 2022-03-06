# Generated by Django 4.0.2 on 2022-02-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='value',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Miscs', 'Miscs'), ('Vehicules', 'Vehicules'), ('Home', 'Home'), ('Electronics', 'Electronics')], default='Miscs', max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
