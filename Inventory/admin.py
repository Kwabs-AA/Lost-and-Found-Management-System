from django.contrib import admin
from .models import Lost

# Register your models here.

class LostAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'indexNo', 'location')  # Fields to display in the list view
    search_fields = ('category', 'name', 'indexNo', 'location')  # Fields to search by
    list_filter = ('category',)  # Filters for the right sidebar

admin.site.register(Lost, LostAdmin)