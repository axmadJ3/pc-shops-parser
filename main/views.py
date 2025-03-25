from django.shortcuts import render

from main.models import Product

def home(request):
    lastest_products = Product.objects.all().order_by('-created_at')[:8]
    context = {
        'title': 'Home',
        'lastest_products': lastest_products,
    }
    return render(request, 'main/index.html', context=context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'main/about.html', context=context)


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)
