from django.urls import path
from . import views
urlpatterns = [ 
    path('', views.homePage, name='home'),
    path('products.html', views.productsPage, name='products'),
    path('new_search.html', views.newSearch, name='new_search')
]