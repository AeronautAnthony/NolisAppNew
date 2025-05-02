from django.contrib import admin

# Register your models here.

from .models import Ingredients
from .models import Product
from .models import FlavorPreference
admin.site.register(Ingredients)
admin.site.register(Product)
admin.site.register(FlavorPreference)