from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('create-post/', views.create_post, name='create_post'),
    path('tag/<slug:tag_slug>', views.home, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('edit-comment/<str:pk>', views.edit_comment, name='edit_comment'),
    path('delete-comment/<str:pk>', views.delete_comment, name='delete_comment'),
    path('edit-post/<str:pk>', views.edit_post, name='edit_post'),
    path('delete-post/<str:pk>', views.delete_post, name='delete_post'),
]