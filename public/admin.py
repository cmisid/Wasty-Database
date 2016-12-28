from django.contrib import admin
from django.contrib.gis.db import models as geo
from django.forms.widgets import Textarea

from .models import Item
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'date_joined'
    )

    ordering = (
        'first_name',
        'last_name'
    )

    search_fields = list_display
    ordering = list_display


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'pub_date',
        'pub_user'
    )

    ordering = (
        'name',
    )

    formfield_overrides = {
        geo.PointField: {'widget': Textarea}
    }

    search_fields = list_display
    ordering = ordering
