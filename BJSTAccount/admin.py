from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UsernameField
from .models import BJSTAccount


class BJSTAccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label="请输入密码", widget=forms.PasswordInput)

    def clean_password2(self):
        # 重写clean方法来校验表单是否正常
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入密码不一样，你是不是笨?")
        return password2

    def save(self, commit=True):
        # 对输入的密码进行保存
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.source = '超级管理员修改'
            user.save()
        return user

    class Meta:
        model = BJSTAccount
        fields = ('email',)


class BJSTAccountChangeForm(UserChangeForm):
    class Meta:
        model = BJSTAccount
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BJSTAccountAdmin(UserAdmin):
    form = BJSTAccountChangeForm
    add_form = BJSTAccountCreationForm
    model = BJSTAccount
    list_display = ('id', 'nickname', 'username', 'email', 'last_login', 'date_joined', 'source', 'avatar')
    list_display_links = ('id', 'username')
    ordering = ('-id',)

    # 在添加用户时使用的字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nickname', 'is_active', 'is_staff')}
        ),
    )

