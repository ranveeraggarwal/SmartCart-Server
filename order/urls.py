from django.conf.urls import patterns, url
from order import views

urlpatterns = patterns(
    '',
    url(r'^make_order/(\w+)$', views.make_order, name='make_order'),
    url(r'^add_item/(\w+)/(\w+)$', views.add_item, name='add_item'),
    url(r'^verify_weight/(\w+)/(\d+)$', views.verify_weight, name='verify_weight'),
)
