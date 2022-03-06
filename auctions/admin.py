from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
