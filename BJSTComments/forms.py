"""
@ author: neo
@ date: 2023-12-16  13:14 
@ file_name: forms.PY
@ github: https://github.com/Underson888/
"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
