from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Product


class PriceRangeFilter(admin.SimpleListFilter):
    title = _("Narxlar Oralig'i")
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('1000000-5000000', _('1,000,000 - 5,000,000')),
            ('5000000-10000000', _('5,000,000 - 10,000,000')),
            ('10000000-20000000', _('10,000,000 - 20,000,000')),
            ('20000000+', _('20,000,000+')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1000000-5000000':
            return queryset.filter(price__gte=1000000, price__lte=5000000).order_by('price')
        if self.value() == '5000000-10000000':
            return queryset.filter(price__gte=5000000, price__lte=10000000).order_by('price')
        if self.value() == '10000000-20000000':
            return queryset.filter(price__gte=10000000, price__lte=20000000).order_by('price')
        if self.value() == '20000000+':
            return queryset.filter(price__gte=20000000).order_by('price')
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('laptop_image','name', 'site', 'formatted_price','updated_at')
    list_display_links = ('name',)
    search_fields = ('site', 'name')
    list_filter = ('site', PriceRangeFilter)
    list_per_page = 15

    def formatted_price(self, obj):
        return f"{intcomma(obj.price)} UZS"
    formatted_price.short_description = _("Narx")

    def laptop_image(self, product: Product):
        if product.image_url:
            return mark_safe(
                f'<img src="{product.image_url}" style="max-width: 150px; height: auto; border-radius: 5px;" />'
            )
        return 'Rasm topilmadi'
    laptop_image.short_description = _("Rasm")
