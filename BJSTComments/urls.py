"""
@ author: neo
@ date: 2023-12-16  13:14 
@ file_name: urls.PY
@ github: https://github.com/Underson888/
"""
from django.urls import path
from . import views

app_name = "BJSTComments"

urlpatterns = [
    path('entry/<int:pk>/comment/', views.add_comment_to_entry, name='add_comment_to_entry'),
    path('entry/<int:pk>/comments/', views.view_comments, name='view_comments'),
]

