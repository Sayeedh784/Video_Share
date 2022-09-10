
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import re_path as url
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',auth_views.LoginView.as_view(template_name='app/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='app/logout.html'),name='logout'),
    path('',include('app.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
