from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from main.models import Product


def home(request):
    lastest_products = Product.objects.all().order_by('-created_at')[:8]
    context = {
        'title': 'Bosh sahifa',
        'lastest_products': lastest_products,
    }
    return render(request, 'main/index.html', context=context)


def products_list(request, site=None, brand=None):
    if query := request.GET.get('query'):
        words = query.split()
        filters = Q()
        for word in words:
            filters &= Q(name__icontains=word)
        products = Product.objects.filter(filters).order_by('price')
    else:
        products = Product.objects.all()

    if site:
        products = products.filter(site=site).order_by('price')
    if brand:
        products = products.filter(name__icontains=brand).order_by('price')

    brands = ['Apple', 'Samsung', 'Huawei', 'Lenovo', 'HP', 'Dell', 'Asus', 'Acer', 'MSI']
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sites = Product.objects.values_list("site", flat=True).distinct()
    context = {
        'title': 'Mahsulotlar',
        'sites': sites,
        'products': page_obj,
        'brands': brands,
        'selected_site': site,
        'selected_brand': brand,
        'page_obj': page_obj
    }
    return render(request, 'main/products_list.html', context=context)


def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    context = {
        'title': 'Noutbuk',
        'product': product,
    }
    return render(request, 'main/product_detail.html', context=context)


def about(request):
    context = {
        'title': 'Biz Xaqimizda',
    }
    return render(request, 'main/about.html', context=context)


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)
