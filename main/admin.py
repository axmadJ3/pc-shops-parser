from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('site', 'name', 'created_at','updated_at')
    search_fields = ('site', 'name')
    list_filter = ('site',)
    list_per_page = 20
