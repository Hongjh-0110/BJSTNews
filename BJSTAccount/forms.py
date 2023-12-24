"""
@ author: neo
@ date: 2023-12-15  9:50 
@ file_name: forms.PY
@ github: https://github.com/Underson888/
"""

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets

from .models import BJSTAccount
from .email import verify


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "用户名或者密码输入错误，你是不是黑客?",
        "inactive": "这个账号被我们删了",
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "巴基斯坦小站用户名", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "巴基斯坦小站密码", "class": "form-control"})


class RegisterForm(UserCreationForm):
    # 对邮件的域进行检测
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '输入你的邮箱'}))
    # 设置头像属性
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # 更新字段属性以匹配前端样式
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '输入用户名'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '输入密码'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入密码'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 验证邮箱是否已存在
        email_is_exist = get_user_model().objects.filter(email=email).exists()
        if email_is_exist:
#            pass
            raise ValidationError("该邮箱在巴基斯坦小站已经存在，请换一个邮箱!")
        return email

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class ForgetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': "请输入新密码"
            }
        ),
    )

    new_password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': "请再次确认密码"
            }
        ),
    )

    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "邮箱"
            }
        ),
    )

    code = forms.CharField(
        label="邮箱验证码",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "在此邮箱验证码"
            }
        ),
    )

    def clean_new_password2(self):
        # 校验输入的面膜是否一致
        password1 = self.data.get("new_password1")
        password2 = self.data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次输入密码不一致，你是不是黑客?")
        password_validation.validate_password(password2)

        return password2

    def clean_email(self):
        user_email = self.cleaned_data.get("email")
        email_is_exist = BJSTAccount.objects.filter(email=user_email).exists()
        if not email_is_exist:
            raise ValidationError("邮箱不存在，你是不是黑客?")
        return user_email

    def clean_code(self):
        code = self.cleaned_data.get("code")
        error = verify(
            email=self.cleaned_data.get("email"),
            code=code,
        )
        if error:
            raise ValidationError(error)
        return code


class ForgetPasswordCodeForm(forms.Form):
    email = forms.EmailField(
        label="邮箱",
    )
