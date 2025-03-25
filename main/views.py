from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from main.models import Product


def home(request):
    lastest_products = Product.objects.all().order_by('-created_at')[:8]
    context = {
        'title': 'Bosh sahifa',
        'lastest_products': lastest_products,
    }
    return render(request, 'main/index.html', context=context)


def products_list(request, site=None):
    products = Product.objects.all()
    if site:
        products = products.filter(site=site)

    paginator = Paginator(products, 12)  # 10 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sites = Product.objects.values_list("site", flat=True).distinct()
    context = {
        'title': 'Mahsulotlar',
        'sites': sites,
        'products': page_obj,
        'selected_site': site,
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
