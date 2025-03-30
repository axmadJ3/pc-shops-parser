from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import NumericRangeFilter

from .models import Product


class PriceRangeFilter(admin.SimpleListFilter):
    title = _('Price Range')
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
            return queryset.filter(price__gte=1000000, price__lte=5000000)
        if self.value() == '5000000-10000000':
            return queryset.filter(price__gte=5000000, price__lte=10000000)
        if self.value() == '10000000-20000000':
            return queryset.filter(price__gte=10000000, price__lte=20000000)
        if self.value() == '20000000+':
            return queryset.filter(price__gte=20000000)
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('site', 'name', 'price','updated_at')
    search_fields = ('site', 'name')
    list_filter = ('site', PriceRangeFilter, ('price', NumericRangeFilter))
    list_per_page = 20
