from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^inventory$', views.inventory),
    url(r'^productpage$', views.productpage),
    url(r'^description/(?P<id>\d+)$', views.description),
    url(r'^shoppingcart$', views.shoppingcart),
    url(r'^shoppingcart/(?P<id>\d+)$', views.shoppingcart),
    url(r'^admin$', views.admin),
    url(r'^orders$', views.orders),
    url(r'^orders/(?P<id>\d+)/$', views.display),
    url(r'^products$', views.products),
    url(r'^checkout$', views.checkout),
    url(r'^addproduct$', views.addproduct),
    url(r'^delete$', views.delete),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]
