from django.contrib import admin

# Register your models here.
from .models import Hardware,RF

class Rf_Incline(admin.TabularInline):
    model = RF


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        Rf_Incline,
    ]   
    fields = ['project']

admin.site.register(Hardware,AuthorAdmin)