from django.shortcuts import render, redirect, get_object_or_404
import os
from BJSTComments.forms import CommentForm
from .models import Topic, Entry
from .forms import EntryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from BJSTAccount.models import BJSTAccount
import markdown as md
from haystack.query import SearchQuerySet
from django.urls import reverse


# Create your views here.
def index(request):
	entries = Entry.objects.order_by('-date_added')
	hot_entries = Entry.objects.order_by('-views')
	context = {'entries': entries, 'hot_entries': hot_entries}
	return render(request, 'BJSTArticle/index.html', context)


def topic(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	entries_list = topic.entry_set.order_by('-date_added')
	entries_per_page = 5
	paginator = Paginator(entries_list, entries_per_page)
	page = request.GET.get('page')
	try:
		entries = paginator.page(page)
	except PageNotAnInteger:
		# 如果页码不是整数，显示第一页
		entries = paginator.page(1)
	except EmptyPage:
		# 如果页码超出范围，显示最后一页
		entries = paginator.page(paginator.num_pages)

	context = {'topic': topic, 'entries': entries}
	return render(request, 'BJSTArticle/topic.html', context)


def entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    comments = entry.comment_set.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = entry
            comment.comment_author = request.user
            comment.save()
            return redirect('BJSTArticle:entry', entry_id=entry.id)
    else:
        comment_form = CommentForm()

    # Convert Markdown to HTML with custom CSS
    custom_css = """
        <style>
        img.markdown-content  {
            width: 50%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        </style>
    """

    # 将Markdown内容中的<img>标签添加class
    entry_html_content = md.markdown(entry.markdown_content, extensions=['extra', 'codehilite']).replace('<img', '<img class="markdown-content"') + custom_css
    
    # 增加并保存浏览次数
    entry.views += 1
    entry.save()

    # 将条目、渲染后的HTML内容和评论表单传递给模板
    context = {
        'entry': entry,
        'entry_html_content': entry_html_content,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'BJSTArticle/entry.html', context)




def new_entry(request):
	if request.method == 'POST':
		form = EntryForm(request.POST, request.FILES)
		if form.is_valid():
			entry = form.save(commit=False)
			entry.author = request.user
			form.save()
			return redirect('BJSTArticle:index')
	else:
		form = EntryForm(initial={'author': request.user})
	context = {'form': form}
	return render(request, 'BJSTArticle/new_entry.html', context)


def self_entry(request, user):
	# 获取对应用户的 BJSTAccount 对象
	author = get_object_or_404(BJSTAccount, username=user)
	# 使用获取的 BJSTAccount 对象过滤 Entry 对象
	self_entry = Entry.objects.filter(author=author)
	entries_list = self_entry.order_by('-date_added')
	entries_per_page = 5
	paginator = Paginator(entries_list, entries_per_page)
	page = request.GET.get('page')
	try:
		entries = paginator.page(page)
	except PageNotAnInteger:
		# 如果页码不是整数，显示第一页
		entries = paginator.page(1)
	except EmptyPage:
		# 如果页码超出范围，显示最后一页
		entries = paginator.page(paginator.num_pages)

	context = {'entries': entries, 'author': author}
	return render(request, 'BJSTArticle/self_entry.html', context)


def edit_entry(request, entry_id):
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(data=request.POST, files=request.FILES, instance=entry)
		if form.is_valid():
			# 检查是否上传了新图像
			new_image = request.FILES.get('image')
			if new_image:
				# 删除旧图像文件
				old_image_path = entry.image.path
				if os.path.exists(old_image_path):
					os.remove(old_image_path)
				entry.image = new_image
			form.save()
			return redirect('BJSTArticle:self_entry', user=entry.author)
	context = {'form': form, 'topic': topic, 'entry': entry}
	return render(request, 'BJSTArticle/edit_entry.html', context)


def search(request):
	query = request.GET.get('q', '')
	results = SearchQuerySet().filter(content__iexact=query).load_all()

	context = {
		'query': query,
		'results': results,
	}

	return render(request, 'search/search.html', context)


def delete_entry(request, entry_id):
	# 根据 entry_id 获取需要删除的文章
	entry = Entry.objects.get(id=entry_id)
	# 调用.delete()方法删除文章
	entry.delete()
	# 完成删除后重定向到生成的 URL
	return redirect('BJSTArticle:self_entry', user=entry.author)


def profile(request):
	# 获取对应用户的 BJSTAccount 对象
	author = request.user
	# 使用获取的 BJSTAccount 对象过滤 Entry 对象
	self_entry = Entry.objects.filter(author=author)
	entries = self_entry.order_by('-views')
	context = {'entries': entries, }
	return render(request, 'BJSTArticle/profile.html', context)
