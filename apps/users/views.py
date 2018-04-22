import re

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from apps.users.models import User
from celery_tasks.tasks import send_active_mail
from dailyfresh import settings
from utils.common import LoginAuthenticateMixin


class RegisterView(View):
    """注册类的类试图"""

    def get(self, request):
        """注册页面"""
        return render(request, 'users/register.html')

    def post(self, request):
        """用户提交注册数据"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 判断用户名是否为空
        if not all([username, password, password2, email]):
            return render(request, 'users/register.html', {'message': '用户名输入为空！'})

        # 判断两次密码是否输入正确
        if password != password2:
            return render(request, 'users/register.html', {'message': '两次输入的密码不同！'})

        # 验证邮箱是否输入正确
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'users/register.html', {'message': '邮箱格式不正确'})

        # 判断是否勾选了协议
        if allow != 'on':
            return render(request, 'users/register.html', {'message': '请先同意用户协议'})

        # 保存用户到数据库中
        # create_user: 是django提供的方法, 会对密码进行加密后再保存到数据库
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
            User.objects.filter(id=user.id).update(is_active=False)
        except IntegrityError:
            return render(request, 'users/register.html', {'message': '用户名已存在'})

        # todo: 发送邮件
        token = user.generate_active_token()
        # send_active_email(username, email, token)
        # celery异步发送邮件
        send_active_mail.delay(username, email, token)

        # return HttpResponse('请登录首页')
        return redirect(reverse("users:login"))


class LoginView(View):
    """登陆类视图"""

    def get(self, request):
        """get请求处理函数"""
        return render(request, 'users/login.html')

    def post(self, request):
        """post请求处理函数"""
        # 获取参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # todo:参数校验
        # 用户名密码是否为空
        if not all([username, password]):
            return render(request, 'users/login.html',
                          {'message': '用户名或者密码不能为空！'})

        # 调用 django 提供的authenticate方法，校验用户名与密码是否匹配
        user = authenticate(username=username, password=password)
        # 用户是否注册
        if user is None:
            return render(request, 'users/login.html',
                          {'message': '用户名或密码不正确！'})

        # 检验账户是否激活
        if not user.is_active:
            return render(request, 'users/login.html',
                          {'message': '账户未激活请先激活用户！'})

        # 判断是否勾选了保存登陆状态
        if remember != 'on':
            # 没有勾选保存session
            request.session.set_expiry(0)
        else:
            # 勾选保存十天免登陆
            request.session.set_expiry(3600*24*10)

        # 通过django的login方法，保存登录用户状态（使用session）
        login(request, user)
        print(request.session)
        # 返回首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    """用户激活 处理类"""

    def get(self, request, token: str):
        try:
            s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
            info = s.loads(token)
            user_id = info['confirm']
        except SignatureExpired:
            # todo:激活链接失效  后期重定向到发送邮件界面
            return HttpResponse("链接已经过期，请重新发送激活邮件!")

        # 修改用户激活状态
        User.objects.filter(id=user_id).update(is_active=True)

        # 激活成功，重定向到登陆页面
        return redirect(reverse('users:login'))


class UserInfoView(LoginAuthenticateMixin, View):
    """用户信息视图"""

    def get(self, request):
        context = {
            'which_code': 1
        }
        print(UserInfoView.__mro__)
        return render(request, 'users/user_center_info.html', context)


class UserOrderView(LoginAuthenticateMixin, View):
    """用户订单视图"""

    def get(self, request):
        context = {
            'which_code': 2
        }
        return render(request, 'users/user_center_order.html', context)


class UserAddressView(View, LoginAuthenticateMixin):
    """用户地址视图"""

    def get(self, request):
        print(UserAddressView.__mro__)
        context = {
            'which_code': 3
        }
        return render(request, 'users/user_center_site.html', context)


class LogoutView(View):
    """注销用户操作"""

    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))
