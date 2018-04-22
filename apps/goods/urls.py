from django.conf.urls import include, url

from apps.goods import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]
