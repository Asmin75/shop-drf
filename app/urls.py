from django.urls import path, re_path
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
    re_path('test/(?P<uid>[0-9A-Za-z]+)/$', views.passwordresetdone_view, name='password_reset_done'),

    # path('index/', views.index),
    path('', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)