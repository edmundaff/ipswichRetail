from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.catalogue, name='catalogue'),
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),
    path('basket/', views.basket_view, name='basket'),
    path('basket/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('basket/update/<int:product_id>/', views.basket_update, name='basket_update'),
    path('basket/checkout/', views.demo_checkout, name='demo_checkout'),
    path('health/', views.health, name='health'),
]
