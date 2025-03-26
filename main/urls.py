from django.urls import path

from main import views

namespace = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products_list, name='products-list'),
    path('products/site/<str:site>/', views.products_list, name='products-list-filtered'),
    path('products/brand/<str:brand>/', views.products_list, name='products-list-filtered-brand'),
    path('products/site/<str:site>/brand/<str:brand>/', views.products_list, name='products-list-filtered-both'),
    path('product/<int:product_pk>/', views.product_detail, name='product-detail'),
]


handler404 = views.custom_page_not_found
