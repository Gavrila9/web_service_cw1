from django.contrib import admin

# Register your models here.
from .models import Professors, Moudles, Rating, Users
admin.site.register(Professors)
admin.site.register(Moudles)
admin.site.register(Rating)
admin.site.register(Users)

