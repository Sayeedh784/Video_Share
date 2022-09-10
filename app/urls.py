from django.contrib import admin
from django.urls import path,include
from app import views
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.home, name="home"),
  path('signup/',views.user_signup,name="signup"),
  path('profile/<int:id>/', views.profile,name="profile"),
  path('profileid/<str:pk>/', views.seeprofile,name="profileid"),
  path('update/<int:pk>/',views.UserUpdateView.as_view(),name="update"),
  # path('post/', views.post,name="post"),
  path('post/',views.VideoPostCreateView.as_view(),name='post'),
  path('video-detail/<int:pk>/',VideoDetailView.as_view(), name='video-detail'),
  path('video-update/<int:pk>/edit/',VideoUpdateView.as_view(), name='video-edit'),
  path('video-delete/<int:pk>/delete/',VideoDeleteView.as_view(), name='video-delete'),
  path('post/<int:pk>/like', AddLike.as_view(), name='like'),
  path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
  
  path('search_list/',views.search_list,name="search_list"),

  
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)