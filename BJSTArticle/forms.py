from django import forms
from .models import Topic, Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['topic', 'title', 'image', 'markdown_content']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '标题', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'image/jpeg, image/png'}),
            'markdown_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'placeholder': '尽情使用md语法!',
                                                      'required': True}),
        }
