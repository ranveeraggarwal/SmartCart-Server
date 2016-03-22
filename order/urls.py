from django.conf.urls import patterns, url
from order import views

urlpatterns = patterns(
    '',
    url(r'^make_order/(\d+)$', views.make_order, name='make_order'),
    url(r'^add_item/(\d+)/(\d+)$', views.add_item, name='add_item'),
)
