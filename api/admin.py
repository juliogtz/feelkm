from django.contrib import admin

# Register your models here.
from .models import events, users, comments_events

admin.site.register(events)
admin.site.register(users)
admin.site.register(comments_events)