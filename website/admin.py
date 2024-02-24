from django.contrib import admin
from website.models import CustomUser
from django.utils.html import format_html
# Register your models here.
@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ('name', 'phone', 'birth_date', 'age', 'marks','is_admin','is_student')
