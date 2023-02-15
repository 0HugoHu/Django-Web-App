from django.contrib import admin

from .models import User, Trip, Vehicle

admin.site.register(User)
admin.site.register(Trip)
admin.site.register(Vehicle)

