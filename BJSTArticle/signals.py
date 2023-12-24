from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Topic

# 定义默认的主题列表
DEFAULT_TOPICS = ['文化', '国际', '社会']

@receiver(post_migrate)
def create_default_topics(sender, **kwargs):
    # 检查数据库中是否已存在主题
    existing_topics = Topic.objects.filter(text__in=DEFAULT_TOPICS)

    # 如果不存在，则创建默认主题
    for topic_text in DEFAULT_TOPICS:
        if not existing_topics.filter(text=topic_text).exists():
            Topic.objects.create(text=topic_text)

# 导入该信号接收器
