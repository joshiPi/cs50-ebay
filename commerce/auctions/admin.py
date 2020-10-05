from django.contrib import admin

# Register your models here.
from .models import Listings
from .models import Comments

admin.site.register(Listings)

admin.site.register(Comments)
