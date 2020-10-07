from django.contrib import admin

# Register your models here.
from .models import Listings, Comments, Bids

admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bids)
