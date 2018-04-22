from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'goods/index.html', {'titiel': '首页'})
