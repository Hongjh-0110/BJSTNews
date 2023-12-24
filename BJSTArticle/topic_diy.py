from .models import Topic  # 导入您的模型


def topics(request):
	topic = Topic.objects.order_by('date_added')  # 获取数据库中的数据
	return {'topics': topic}
