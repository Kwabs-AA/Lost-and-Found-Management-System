from django.contrib import admin
from .models import Lost,Review,Badges

# Register your models here.

class LostAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'indexNo', 'location','uploader_name')  # Fields to display in the list view
    search_fields = ('category', 'name', 'indexNo', 'location')  # Fields to search by
    list_filter = ('category',)  # Filters for the right sidebar

admin.site.register(Lost, LostAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display=('reviewer_name','rating','review_text','uploader_name','created_at')
    list_filter=('rating',)

admin.site.register(Review,ReviewAdmin)


class BadgesAdmin(admin.ModelAdmin):
    list_display=('count','uploader_name')

admin.site.register(Badges,BadgesAdmin)