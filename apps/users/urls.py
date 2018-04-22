from django.conf.urls import include, url

from apps.users import views

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^do_register$', views.do_register, name='do_register'),

    url(r'^register$', views.RegisterView.as_view(), name='register'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    # 激活邮件
    url(r'^active/(.+)$', views.ActiveView.as_view(), name='active'),


    # 用户中心
    url(r'^$', views.UserInfoView.as_view(), name='user'),
    url(r'^order$', views.UserOrderView.as_view(), name='order'),
    url(r'^address$', views.UserAddressView.as_view(), name='address'),
]
