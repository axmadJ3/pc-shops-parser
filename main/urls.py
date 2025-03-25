from django.urls import path

from main import views

namespace = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products_list, name='products_list'),
]

handler404 = views.custom_page_not_found
