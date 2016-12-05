from django.contrib import admin

from .models import Item
from .models import Person


admin.site.register(Item)
admin.site.register(Person)
