from django.contrib.auth.decorators import login_required


class LoginAuthenticateMixin(object):
    """登陆检查类"""

    @classmethod
    def as_view(cls, **initkwargs):
        view_func = super().as_view(**initkwargs)
        return login_required(view_func)
