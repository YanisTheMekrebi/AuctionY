from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

import datetime


CATEGORY_CHOICES = [
    ("Miscs", "Miscs"),
    ("Vehicules", "Vehicules"),
    ("Home", "Home"),
    ("Electronics", "Electronics"),
    ("Fashion", "Fashion"),
    ("Toys", "Toys"),
    ("Video Games", "Video Games"),
    ("Cooking", "Cooking"),
    ("Study", "Study"),
]


class User(AbstractUser):
    pass


class Listing(models.Model):
    date_created = models.DateField(default=datetime.date.today)
    seller = models.ForeignKey('User', on_delete=models.CASCADE, related_name='listings')
    closed = models.BooleanField(default=False)
    watchlisting_users = models.ManyToManyField('User', related_name="watchlist", blank=True)
    product_name = models.CharField(max_length=64)
    description = models.TextField(max_length=400)
    # Note that the optimal image size is 230x200 px, you may want to let the user know this in the future.
    image_url = models.URLField(blank=True, default='')
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, default='Miscs')

    def get_highest_bid(self):
        return self.bids.order_by('-value')[0]

    def __str__(self):
        return f"{self.product_name}"


class Bid(models.Model):
    date_created = models.DateField(auto_now_add=True)
    bidder = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bids')
    value = models.FloatField(validators=[MinValueValidator(0.99)])

    def __str__(self):
        return f"Bid of {self.value}$ to '{self.listing.product_name}' by {self.bidder}"


class Comment(models.Model):
    date_created = models.DateField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=200)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment to {self.listing} by {self.commenter}"
