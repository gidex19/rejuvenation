from django.contrib import admin
from .models import Profile, UserFollowers

admin.site.register(UserFollowers)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','image')

