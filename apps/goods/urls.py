from django.conf.urls import include, url

from apps.goods import views

urlpatterns = [
    url(r'^index$', views.IndexView.as_view(), name='index'),
    url(r'^detail/(\d+)$', views.DetailView.as_view(), name='detail'),
    url(r'^list/(\d+)/(\d*)$', views.ListView.as_view(), name='list'),
    # url(r'^$', views.IndexView.as_view(), name='index'),
]
