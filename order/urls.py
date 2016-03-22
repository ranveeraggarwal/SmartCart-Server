from django.conf.urls import patterns, url
from order import views

urlpatterns = patterns(
    '',
    url(r'^(\d+)$', views.make_order, name='index'),
)
