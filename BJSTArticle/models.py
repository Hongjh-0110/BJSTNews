from django.db import models
from BJSTAccount.models import BJSTAccount
import markdown as md

# Create your models here.
class Topic(models.Model):  # 主题
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Entry(models.Model):
    # 具体的新闻
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(BJSTAccount, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    # 使用markdown形式
    markdown_content = models.TextField()
    # text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', default=None)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'entries'

    def get_html_content(self):
        return md.markdown(self.markdown_content, extensions=['extra', 'codehilite'])

    def __str__(self):
        return f"{self.title[:50]}"

