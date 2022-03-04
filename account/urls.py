from django.urls import path, include
from . import views
from django.contrib.auth import urls
app_name = 'account'


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('edit/', views.edit, name='edit'),
    path('', include('django.contrib.auth.urls')),
    path('manage-posts/', views.post_manager, name='post_manager'),
    path('delete-account/<int:pk>/', views.DeleteView.as_view(), name='delete_account'),
]
