from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

# from tutorial.snippets.views import registration_view

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    # path('post-create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    # path('post-update/<int:pk>/', views.PostUpdateDestroy.as_view(), name='post-update-destroy'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('register/', views.registration_view, name='register'),
    path('password_reset/', views.passwordreset_view, name='password_reset'),
    # path('password_reset_confirm/', views.passwordresetconfirm_view, name='password_reset_confirm')

    # path('index/', views.index),
    path('', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)