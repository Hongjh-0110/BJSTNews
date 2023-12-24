# BTSTUser/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.sites.models import Site
from functools import lru_cache


# 巴基斯坦小站优化点1
# 引入缓存器能够提高网页加载性能
@lru_cache()
def get_current_site():
    site = Site.objects.get_current()
    return site


class BJSTAccount(AbstractUser):
    nickname = models.CharField('nick name', max_length=100, blank=True)
    creation_time = models.DateTimeField('creation time', default=now)
    last_modify_time = models.DateTimeField('last modify time', default=now)
    source = models.CharField('create source', max_length=100, blank=True)
    # 增加头像
    avatar = models.ImageField('avatar', upload_to='avatar/', default='avatar/avatar1.jpg')

    def get_absolute_url(self):
        return reverse('BJSTArticle:author_detail', kwargs={'author_name': self.username})

    def get_full_url(self):
        site = get_current_site().domain
        url = f"https://{site}{self.get_absolute_url()}"
        return url

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = 'user'
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="bjstaccount_set",  # 添加 unique related_name
        related_query_name="bjstaccount",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="bjstaccount_set",  # 添加 unique related_name
        related_query_name="bjstaccount",
    )

