from django.contrib import admin

# Register your models here.
from rtc.models import Room

admin.site.register(
    Room,
    list_display=["id", "title", "staff_only"],
    list_display_links=["id", "title"],
)