from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import *


class ListingForm(forms.ModelForm):
    starting_bid = forms.FloatField(min_value=0.99)

    class Meta:
        model = Listing
        exclude = ["date_created", "seller", "watchlisting_users", "closed"]
    
    field_order = ["starting_bid"]


class PlaceBidForm(forms.ModelForm):
    confirm_bid = forms.FloatField(min_value=0.99)

    class Meta:
        model = Bid
        fields = ["value", "confirm_bid"]
        labels = {
            "value": "Place Bid"
        }

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop("listing")
        super(PlaceBidForm, self).__init__(*args, **kwargs)

    def clean_value(self):
        value = self.cleaned_data["value"]
        if value <= self.listing.get_highest_bid().value:
            raise ValidationError(
                "Bid must be greater than the current price."
            )
        
        return value

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get("value")
        confirm_bid = cleaned_data.get("confirm_bid")
        
        if value and confirm_bid:
            if value != confirm_bid:
                raise ValidationError(
                    "Bids must match."
                )


class ListingAdmin(admin.ModelAdmin):
    form = ListingForm
    exclude = ["date_created"]

    def save_model(self, request, obj, form, change):
        if not change:
            new_bid = Bid(bidder=obj.seller, listing=obj, value=form.cleaned_data["starting_bid"])
            super().save_model(request, obj, form, change)
            new_bid.save()
