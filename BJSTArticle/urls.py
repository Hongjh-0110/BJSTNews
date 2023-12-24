from django.urls import path
from . import views

app_name = 'BJSTArticle'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('entries/<int:entry_id>/', views.entry, name='entry'),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('self_entry/<str:user>', views.self_entry, name='self_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('profile/', views.profile, name='profile'),
]
