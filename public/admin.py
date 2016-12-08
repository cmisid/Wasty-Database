from django.contrib import admin

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
        'little_description',
        'pub_date',
        'pub_user',
        'render_image'
    )

    ordering = (
        'name',
    )

    search_fields = list_display
    ordering = ordering
