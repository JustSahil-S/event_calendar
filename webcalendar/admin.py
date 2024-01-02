from django.contrib import admin
from .models import User, Calendar, Event

admin.site.register(User)
admin.site.register(Calendar)
admin.site.register(Event)

# Register your models here.
