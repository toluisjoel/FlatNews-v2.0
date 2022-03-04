from django.contrib import admin
from .models import Profile
# Register your models here.


@admin.register(Profile)
class ProfileAdminModel(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'profile_picture', 'gender')
