
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',auth_views.LoginView.as_view(template_name='app/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='app/logout.html'),name='logout'),
    path('',include('app.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
