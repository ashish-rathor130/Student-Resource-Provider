from django.contrib import admin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    fields = ['username','email','is_email_verified','otp_last_sent']
    
admin.site.register(CustomUser,CustomUserAdmin)
