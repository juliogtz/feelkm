from django.contrib import admin

# Register your models here.
from .models import events, users

admin.site.register(events)
admin.site.register(users)