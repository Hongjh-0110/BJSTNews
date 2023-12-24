from .models import Entry
from haystack import indexes


# !!!类名必须为需要检索的ModelName+Index
class EntryIndex(indexes.SearchIndex, indexes.Indexable):
	# 创建一个用于接收搜索框内容的字段text
	# use_template根据哪些字段建立索引，将说明放入一个文件中
	text = indexes.CharField(document=True, use_template=True)

	# 重载get_model方法！
	def get_model(self):
		return Entry

	# 建立索引的数据
	def index_queryset(self, using=None):
		return self.get_model().objects.all()
