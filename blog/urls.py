from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('<published_date>/<slug>/<str:pk>', views.post_detail, name='post_detail'),
    path('create-post/', views.CreatePostView.as_view(), name='create_post'),
    # path('tag/<slug:tag_slug>', views.Tags.as_view(), name='post_list_by_tag'),
    path('edit-comment/<str:pk>', views.EditCommentView.as_view(), name='edit_comment'),
    path('delete-comment/<str:pk>', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('edit-post/<str:pk>', views.EditPostView.as_view(), name='edit_post'),
    path('delete-post/<str:pk>', views.DeletePostView.as_view(), name='delete_post'),
]