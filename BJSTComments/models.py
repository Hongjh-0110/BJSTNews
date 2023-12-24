# Create your models here.
from django.contrib.auth.models import User
from BJSTArticle.models import Entry

from django.db import models
from BJSTArticle.models import Entry
from BJSTAccount.models import BJSTAccount


class Comment(models.Model):
    article = models.ForeignKey(to=Entry, on_delete=models.CASCADE, verbose_name='评论文章')
    comment_content = models.TextField(verbose_name='评论内容')
    comment_author = models.ForeignKey(to=BJSTAccount, on_delete=models.CASCADE, verbose_name='评论者')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    # 父级评论，如果没有父级则为空NULL, "self"表示外键关联自己
    pre_comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True,
                                    verbose_name='父评论id')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
