# Generated by Django 4.0.2 on 2022-03-04 13:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_bidder_alter_bid_listing_alter_bid_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlisted_by',
            field=models.ManyToManyField(related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
