from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from BJSTArticle.models import Entry
from .models import Comment


def add_comment_to_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = entry
            comment.comment_author = request.user
            comment.save()
            return redirect('BJSTArticle:entry', entry_id=entry.id)
    else:
        form = CommentForm()

    return render(request, 'BJSTArticle/entry.html', {
        'form': form,
        'entry': entry,
        'comments': Comment.objects.filter(article=entry)
    })


def view_comments(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    comments = Comment.objects.filter(article=entry)
    return render(request, 'BJSTArticle/entry.html', {'entry': entry, 'comments': comments})
