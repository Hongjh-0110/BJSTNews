from django.shortcuts import render
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
# 发送邮件
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .email import get_sha256, get_current_site, generate_code, send_verify_email, set_code
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ForgetPasswordCodeForm
from .models import BJSTAccount


# Create your views here.
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'BJSTAccount/registration.html'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(False)
            user.is_active = False
            user.source = 'Register'

            # 添加头像注册功能
            if 'avatar' in self.request.FILES:
                user.avatar = self.request.FILES['avatar']

            user.save(True)
            site = get_current_site().domain
            sign = get_sha256(get_sha256(settings.SECRET_KEY + str(user.id)))

            if settings.DEBUG:
                site = '123.249.111.181:8000'
            path = reverse('BJSTAccount:result')
            url = "http://{site}{path}?type=validation&id={id}&sign={sign}".format(
                site=site, path=path, id=user.id, sign=sign)

            content = """
                            请点击下面链接验证您的邮箱:
                            
                            --------- {url} ---------
                            """.format(url=url)
            print(send_mail(
                from_email="djangotest8882023@163.com",
                subject='验证电子邮箱',
                message=content,
                recipient_list=[user.email]
            ))

            url = reverse('BJSTAccount:result') + \
                  '?type=register&id=' + str(user.id)
            return HttpResponseRedirect(url)
        else:
            return self.render_to_response({
                'form': form
            })


class LogoutView(RedirectView):
    url = '/login/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'BJSTAccount/login.html'
    success_url = '/'
    redirect_field_name = REDIRECT_FIELD_NAME
    login_ttl = 10800

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        kwargs['redirect_to'] = redirect_to

        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):

        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            auth.login(self.request, form.get_user())
            if self.request.POST.get("remember"):
                self.request.session.set_expiry(self.login_ttl)
            return super(LoginView, self).form_valid(form)
        else:

            return self.render_to_response({
                'form': form
            })

    def form_invalid(self, form):
        # 添加 form_submitted 标志
        return self.render_to_response(self.get_context_data(form=form, form_submitted=True))

    def get_success_url(self):

        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not url_has_allowed_host_and_scheme(
                url=redirect_to, allowed_hosts=[
                    self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to


def account_result(request):
    # 获取传入的信息
    type = request.GET.get('type')
    id = request.GET.get('id')
    user = get_object_or_404(get_user_model(), id=id)
    if user.is_active:
        return HttpResponseRedirect('/')
    if type and type in ['register', 'validation']:
        if type == 'register':
            content = '''
        你小子已注册成功，一封验证邮件已经发送到你的邮箱，请验证后登录本站!
            '''
            title = '注册成功'
        else:
            c_sign = get_sha256(get_sha256(settings.SECRET_KEY + str(user.id)))
            sign = request.GET.get('sign')
            if sign != c_sign:
                return HttpResponseForbidden()
            user.is_active = True
            user.save()
            content = '''
                完成邮箱验证!你小子现在可以使用你的账号来登录巴基斯坦小站！
            '''
            title = '验证成功'
        return render(request, 'BJSTAccount/result.html', {
            'title': title,
            'content': content
        })
    else:
        return HttpResponseRedirect('/')


class ForgetPasswordView(FormView):
    form_class = ForgetPasswordForm
    template_name = 'BJSTAccount/forget_password.html'

    def form_valid(self, form):
        if form.is_valid():
            user = BJSTAccount.objects.filter(email=form.cleaned_data.get("email")).get()
            user.password = make_password(form.cleaned_data["new_password2"])
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            return self.render_to_response({'form': form})


class ForgetPasswordEmailCode(View):
    def post(self, request: HttpRequest):
        form = ForgetPasswordCodeForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'message': '邮箱错误!', 'status': 'error'})

        to_email = form.cleaned_data["email"]
        code = generate_code()
        send_verify_email(to_email, code)
        set_code(to_email, code)

        return JsonResponse({'message': '验证码发送成功！', 'status': 'success'})

