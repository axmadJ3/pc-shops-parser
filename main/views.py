from django.shortcuts import render


def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'main/index.html', context=context)


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)
