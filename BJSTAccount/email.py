"""
@ author: neo
@ date: 2023-12-15  10:55 
@ file_name: email.PY
@ github: https://github.com/Underson888/
"""
import random
import string
import typing
from datetime import timedelta
from hashlib import sha256

import django.dispatch
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.translation import gettext

_code_ttl = timedelta(minutes=5)

send_email_signal = django.dispatch.Signal(
    ['emailto', 'title', 'content'])


def send_verify_email(to_mail: str, code: str, subject: str = "验证邮件的方式"):
    html_content = "重新设定的密码是:%(code)s" % {'code': code}
    print(send_mail(
        recipient_list=[to_mail],
        message=html_content,
        from_email="djangotest8882023@163.com",
        subject=subject
    ))


def verify(email: str, code: str) -> typing.Optional[str]:
    cache_code = get_code(email)
    if cache_code != code:
        return gettext("验证错误!")


def set_code(email: str, code: str):
    cache.set(email, code, _code_ttl.seconds)


def get_code(email: str) -> typing.Optional[str]:
    return cache.get(email)


def get_sha256(str):
    m = sha256(str.encode('utf-8'))
    return m.hexdigest()


def cache_decorator(expiration=3 * 60):
    def wrapper(func):
        def news(*args, **kwargs):
            try:
                view = args[0]
                key = view.get_cache_key()
            except:
                key = None
            if not key:
                unique_str = repr((func, args, kwargs))

                m = sha256(unique_str.encode('utf-8'))
                key = m.hexdigest()
            value = cache.get(key)
            if value is not None:
                # logger.info('cache_decorator get cache:%s key:%s' % (func.__name__, key))
                if str(value) == '__default_cache_value__':
                    return None
                else:
                    return value
            else:
                value = func(*args, **kwargs)
                if value is None:
                    cache.set(key, '__default_cache_value__', expiration)
                else:
                    cache.set(key, value, expiration)
                return value

        return news

    return wrapper


@cache_decorator()
def get_current_site():
    site = Site.objects.get_current()
    return site


def generate_code() -> str:
    """生成随机数验证码"""
    return ''.join(random.sample(string.digits, 6))
