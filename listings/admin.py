from django.contrib import admin

from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_publised', 'price', 'listing_date', 'realtor')
    list_display_links = ('id', 'title')
    list_editable = ['is_publised']
    search_fields = ('id', 'title', 'description',)
    list_per_page = 25


admin.site.register(Listing, ListingAdmin)
